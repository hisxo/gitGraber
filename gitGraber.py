#!/usr/bin/python3

import requests
import re
import json
import time
import argparse
import mmap
import argcomplete
import config
import tokens
import os
import time
from datetime import datetime
from pprint import pprint
from termcolor import colored
from urllib.parse import urlparse

def createEmptyBinaryFile(name):
    f = open(name, 'wb')
    f.write(1*b'\0')
    f.close()

def initFile(name):
    if not name or os.path.getsize(name) == 0:
        createEmptyBinaryFile(name)

def clean(result):
    cleanToken = re.sub(tokens.CLEAN_TOKEN_STEP1, '', result.group(0))
    return re.sub(tokens.CLEAN_TOKEN_STEP2, '', cleanToken)

def checkToken(content, tokensMap, tokensCombo):
    tokensFound = {}
    # For each type of tokens (ie 'AWS'...)
    for token in tokensMap:
        regexPattern = re.compile(token.getRegex())
        # Apply the matching regex on the content of the file downloaded from GitHub
        result = re.search(regexPattern, content)
        # If the regex matches, add the result of the match to the dict tokens and the token name found
        if result:
            cleanToken = clean(result) 
            blacklist = token.getBlacklist()
            foundbl = False
            if blacklist:
                for blacklistedPattern in blacklist:
                    if blacklistedPattern in cleanToken:
                        foundbl = True
                if not foundbl:
                    tokensFound[cleanToken] = token.getName()
    
    for combo in tokensCombo:
        found = True
        result = [''] * len(combo.getTokens())
        for t in combo.getTokens():
            regexPattern = re.compile(t.getRegex())
            match = re.search(regexPattern, content)
            if not match:
                found = False
                break
            result[t.getDisplayOrder()-1] = clean(match)
        if found:
            concatToken = ":".join(result)
            tokensFound[concatToken] = combo.getName()

    return tokensFound

def notifySlack(message):
    if not config.SLACK_WEBHOOKURL:
        print('Please define Slack Webhook URL to enable notifications')
        exit()
    requests.post(config.SLACK_WEBHOOKURL, json={'text': ':new:'+message})

def writeToWordlist(content, wordlist):
    f = open(wordlist, 'a+')
    s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    filename = content.split('/')[-1]
    if s.find(bytes(filename,'utf-8')) == -1:
        f.write(filename + '\n')

def displayResults(result, tokenResult, rawGitUrl, urlInfos):
    possibleTokenString = '[!] POSSIBLE '+tokenResult[result]+' TOKEN FOUND (keyword used:'+githubQuery+')'
    print(colored(possibleTokenString,'green'))
    commitString = '[+] Commit '+urlInfos[2]+' : '+urlInfos[3]+' by '+urlInfos[4]
    print(commitString)
    urlString = '[+] RAW URL : ' + rawGitUrl
    print(urlString)
    tokenString = '[+] Token : ' + result 
    print(tokenString.strip())
    repoString = '[+] Repository URL : '+urlInfos[1]
    print(repoString)
    return possibleTokenString+'\n'+commitString+'\n'+urlString+'\n'+tokenString+'\n'+repoString

def parseResults(content):
    data = json.loads(content)
    contentRaw = {}
    f = open(config.GITHUB_URL_FILE, 'a+', encoding='utf-8')
    try:
        for item in data['items']:
            gitUrl = item['url']
            repoName = item['repository']['full_name']
			
            #Parse JSON to get info about repository
            response = doRequestGitHub(gitUrl)
            rawUrl = json.loads(response.text)
            rawGitUrl = rawUrl['download_url']
            
            #Request to extract data about repository and user
            commitHash = gitUrl.split('ref=')[1]
            commitUrl = config.GITHUB_API_COMMIT_URL+repoName+'/commits/'+commitHash
            response = doRequestGitHub(commitUrl)
            commitData = json.loads(response.text)
            commitDate = commitData['commit']['author']['date']
            
            #Compare the current date and date of commit
            currentTimestamp = int(time.time())
            timestampCommit = int(time.mktime(datetime.strptime(commitDate, '%Y-%m-%dT%H:%M:%SZ').timetuple()))
            compareCommitDate = (currentTimestamp - timestampCommit)/3600
            
            #Conversion in day if the commit date is > 24h
            if compareCommitDate > 24: 
              compareCommitDate = round(compareCommitDate/24)
              compareCommitDate = '(' + str(compareCommitDate)+' days ago)'
            else:
             compareCommitDate = round(compareCommitDate)
             compareCommitDate = '(' + str(compareCommitDate)+' hours ago)'
            
            #Parse JSON to get the user
            commitAuthor = commitData['commit']['author']['email']
            
            s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            if s.find(bytes(rawGitUrl,'utf-8')) == -1:
               f.write(rawGitUrl + '\n')
               contentRaw[rawGitUrl] = []
               contentRaw[rawGitUrl].append(doRequestGitHub(rawGitUrl))
               contentRaw[rawGitUrl].append(config.GITHUB_BASE_URL+'/'+repoName)
               contentRaw[rawGitUrl].append(compareCommitDate)
               contentRaw[rawGitUrl].append(commitDate)
               contentRaw[rawGitUrl].append(commitAuthor)
        return contentRaw

    except Exception as e:
        print('Exception '+str(e))
        pass

# Transform the config github token list to a dict of key values
def initGithubToken():
    init = []
    for token in config.GITHUB_TOKENS:
        init.append({"token": token, "remaining": 1, "reset": time.time()})
    return init

# Manages a token stores with request remaining count and reset time
# for each github token
def getGithubToken(url):
    minTimeToken = 0
    path = urlparse(url).path
    #pprint(config.GITHUB_TOKENS)
    if not path in config.GITHUB_TOKENS_STATES:
        config.GITHUB_TOKENS_STATES[path] = initGithubToken()

    for tokenState in config.GITHUB_TOKENS_STATES[path]:
        if tokenState['remaining'] > 0:
            return tokenState['token']
        if minTimeToken == 0 or minTimeToken['reset'] > tokenState['reset']:
            minTimeToken = tokenState

    sleepTime = minTimeToken['reset'] - int(time.time()) + 1
    if sleepTime > 0:        
        print('[i] Sleeping ' + str(sleepTime) + ' sec')
        time.sleep(sleepTime)

    return minTimeToken['token']

# Updates github token stores with last response information
def updateGithubToken(url, token, response):
    path = urlparse(url).path
    for i, tokenState in enumerate(config.GITHUB_TOKENS_STATES[path]):
        if token == tokenState['token']:
            if response.status_code != 200:
                tokenState['remaining'] = 0
            elif 'X-RateLimit-Remaining' in response.headers:
                tokenState['remaining'] = int(response.headers['X-RateLimit-Remaining'])
            if 'X-RateLimit-Reset' in response.headers:
                tokenState['reset'] = int(response.headers['X-RateLimit-Reset'])
            elif 'Retry-After' in response.headers:
                tokenState['reset'] = int(time.time()) + 1 + int(response.headers['Retry-After'])
            config.GITHUB_TOKENS_STATES[path][i] = tokenState

def doRequestGitHub(url, verbose=False):
    nbMaxTry = config.GITHUB_MAX_RETRY
    while nbMaxTry > 0:
        token = getGithubToken(url)
        if verbose:
            print(colored('[i] Github query : ' + url, 'yellow'))
        headers = {
            'Accept': 'application/vnd.github.v3.text-match+json',
            'Authorization': 'token ' + token
        }
        try:
            response = requests.get(url, headers=headers)
            nbMaxTry = nbMaxTry - 1
            if verbose:
                print('[i] Status code : ' + str(response.status_code))
            updateGithubToken(url, token, response)
            if response.status_code == 200:
                return response
                
            elif response.status_code == 403:
                #pprint(response.headers)
                responseJson = json.loads(response.text)
                if "API rate limit exceeded" in responseJson['message']:
                    if verbose:
                        print('[i] API rate limit exceeded for token ' + token)
                elif "abuse detection mechanism" in responseJson['message']:
                    if verbose:
                        print('[i] Abuse detection reached for token ' + token)
                else:
                    print(colored('[!] Unexpected response','red'))
                    print(colored(response.text,'red'))
            else:
                print(colored('[!] Unexpected HTTP response ' + str(response.status_code),'red'))
                print(colored(response.text,'red'))

        except UnicodeEncodeError as e:
            # TODO improve exception management
            print(e.msg)
            pass
                        
def searchGithub(keywordsFile, args):
    keywordSearches = []
    tokenMap, tokenCombos = tokens.initTokensMap()

    with open(keywordsFile, 'r') as myfile:
        for keyword in myfile:
            url = config.GITHUB_API_URL + githubQuery +' '+keyword.strip() +config.GITHUB_SEARCH_PARAMS
            response = doRequestGitHub(url, True)
            content = parseResults(response.text)
            if content:
                for rawGitUrl in content.keys():
                    tokensResult = checkToken(content[rawGitUrl][0].text, tokenMap, tokenCombos)
                    for token in tokensResult.keys():
                        displayMessage = displayResults(token, tokensResult, rawGitUrl, content[rawGitUrl])
                        if args.slack:
                            notifySlack(displayMessage)
                        if args.wordlist:
                            writeToWordlist(rawGitUrl, args.wordlist)

    return keywordSearches

parser = argparse.ArgumentParser()
argcomplete.autocomplete(parser)
parser.add_argument('-k', '--keyword', action='store', dest='keywordsFile', help='Specify a keywords file (-k keywordsfile.txt)', default="wordlists/keywords.txt")
parser.add_argument('-q', '--query', action='store', dest='query', help='Specify your query (-q "myorg")')
parser.add_argument('-s', '--slack', action='store_true', help='Enable slack notifications', default=False)
parser.add_argument('-w', '--wordlist', action='store', dest='wordlist', help='Create a wordlist that fills dynamically with discovered filenames on GitHub')
args = parser.parse_args()

if not args.keywordsFile:
    print('No keyword (-k or --keyword) file is specified')
    exit()

if not args.query or args.query == "":
    print('No query (-q or --query) is specified, default query will be used')
    args.query = ' '
    githubQuery = args.query

keywordsFile = args.keywordsFile
githubQuery = args.query
config.GITHUB_TOKENS_STATES = {}


# If wordlist, check if file is binary initialized for mmap 
if(args.wordlist):
    initFile(args.wordlist)

# Init URL file 
initFile(config.GITHUB_URL_FILE)

# Send requests to Github API
responses = searchGithub(keywordsFile, args)
