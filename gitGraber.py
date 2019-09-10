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
from pprint import pprint
from termcolor import colored

def createEmptyBinaryFile(name):
    f = open(name, 'wb')
    f.write(1*b'\0')
    f.close()

def initFile(name):
    if not name or os.path.getsize(name) == 0:
        createEmptyBinaryFile(name)

def checkToken(content, tokensMap):
    tokens = {}
    # For each type of tokens (ie 'AWS'...)
    for token in tokensMap.keys():
        googleUrlFound = False
        googleSecretFound = False
        regexPattern = re.compile(tokensMap[token])
        # Apply the matching regex on the content of the file downloaded from GitHub
        result = re.search(regexPattern, content)
        # If the regex matches, add the result of the match to the dict tokens and the token name found
        if result:
            if token == 'GOOGLE_URL':
                googleUrlFound = True
            elif token == 'GOOGLE_SECRET':
                googleSecretFound = True
            else:
                tokens[result] = token
            if (googleUrlFound and googleSecretFound):
                tokens[result] = 'GOOGLE'
    return tokens

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
    commitString = '[+] Commit date : '+urlInfos[2]+' by '+urlInfos[3]
    print(commitString)
    urlString = '[+] RAW URL : ' + rawGitUrl
    print(urlString)
    cleanToken = re.sub(tokens.CLEAN_TOKEN_STEP1, '', result.group(0))
    cleanToken = re.sub(tokens.CLEAN_TOKEN_STEP2, '', cleanToken)
    tokenString = '[+] Token : ' + cleanToken
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
			
            #Parse JSON to get info about repository
            repoName = item['repository']['full_name']
            commitHash = gitUrl.split('ref=')[1]
            commitUrl = config.GITHUB_API_COMMIT_URL+repoName+'/commits/'+commitHash
			
            # TODO Centralize header management for token auth here (rate-limit more agressive on Github otherwise)
            headers = {'Accept': 'application/vnd.github.v3.text-match+json',
            'Authorization': 'token ' + config.GITHUB_TOKENS[3]
            }
            response = requests.get(gitUrl,headers=headers)
            rawUrl = json.loads(response.text)
            rawGitUrl = rawUrl['download_url']
            
            #Request to extract data about repository and user
            response = requests.get(commitUrl,headers=headers)
            commitData = json.loads(response.text)
            commitDate = commitData['commit']['author']['date']
            commitAuthor = commitData['commit']['author']['email']
            
            s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            if s.find(bytes(rawGitUrl,'utf-8')) == -1:
               f.write(rawGitUrl + '\n')
               contentRaw[rawGitUrl] = []
               contentRaw[rawGitUrl].append(requests.get(rawGitUrl, headers=headers))
               contentRaw[rawGitUrl].append(config.GITHUB_BASE_URL+'/'+repoName)
               contentRaw[rawGitUrl].append(commitDate)
               contentRaw[rawGitUrl].append(commitAuthor)
        return contentRaw
    except KeyError as ke:
        print(colored('[!] Github API rate-limit detected, please retry with other tokens','red'))
        pass
    except Exception as e:
        # TODO Catch rate-limit exception EXCEPTION 'download_url' 'API rate limit exceeded for x.x.x.x (But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)', 'documentation_url': 'https://developer.github.com/v3/#rate-limiting'
        # TODO Catch mmap exception if rawGitUrls is empty (have to be initialized before first use)
        #print('Exception '+str(e.msg))
        pass

# Transform the config github token list to a dict of key values
def initGithubToken():
    for i, token in enumerate(config.GITHUB_TOKENS):
        config.GITHUB_TOKENS[i] = {"token": token, "remaining": 1, "reset": time.time()}

# Manages a token stores with request remaining count and reset time
# for each github token
def getGithubToken():
    minTimeToken = 0
    #pprint(config.GITHUB_TOKENS)
    for tokenState in config.GITHUB_TOKENS:
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
def updateGithubToken(token, response):
    for i, tokenState in enumerate(config.GITHUB_TOKENS):
        if token == tokenState['token']:
            if response.status_code != 200:
                tokenState['remaining'] = 0
            elif 'X-RateLimit-Remaining' in response.headers:
                tokenState['remaining'] = int(response.headers['X-RateLimit-Remaining'])
            if 'X-RateLimit-Reset' in response.headers:
                tokenState['reset'] = int(response.headers['X-RateLimit-Reset'])
            elif 'Retry-After' in response.headers:
                tokenState['reset'] = int(time.time()) + 1 + int(response.headers['Retry-After'])
            config.GITHUB_TOKENS[i] = tokenState

                        
def requestGithub(keywordsFile, args):
    keywordSearches = []
    tokenMap = tokens.initTokensMap()
    with open(keywordsFile, 'r') as myfile:
        for keyword in myfile:
            resquestNotOK = True
            while resquestNotOK:
                token = getGithubToken()
                print(colored('[+] Github query : '+config.GITHUB_API_URL + githubQuery +' '+keyword.strip() +config.GITHUB_SEARCH_PARAMS,'yellow'))
                # TODO Centralize header management for token auth here (rate-limit more agressive on Github otherwise)
                headers = {
                    'Accept': 'application/vnd.github.v3.text-match+json',
                    'Authorization': 'token ' + token
                }
                try:
                    response = requests.get(config.GITHUB_API_URL + githubQuery +' '+keyword.strip() +config.GITHUB_SEARCH_PARAMS, headers=headers)
                    print('[i] Status code : ' + str(response.status_code))
                    updateGithubToken(token, response)
                    if response.status_code == 200:
                        resquestNotOK = False
                        content = parseResults(response.text)
                        if content:
                            for rawGitUrl in content.keys():
                                tokensResult = checkToken(content[rawGitUrl].text, tokenMap)
                                for token in tokensResult.keys():
                                    displayMessage = displayResults(token, tokensResult, rawGitUrl)
                                    if args.slack:
                                        notifySlack(displayMessage)
                                    if args.wordlist:
                                        writeToWordlist(rawGitUrl, args.wordlist)

                    elif response.status_code == 403:
                        #pprint(response.headers)
                        responseJson = json.loads(response.text)
                        if "API rate limit exceeded" in responseJson['message']:
                            print('[i] API rate limit exceeded for token ' + token)
                        elif "abuse detection mechanism" in responseJson['message']:
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
tokenMap = tokens.initTokensMap()
tokensResult = []
initGithubToken()


# If wordlist, check if file is binary initialized for mmap 
if(args.wordlist):
    initFile(args.wordlist)

# Init URL file 
initFile(config.GITHUB_URL_FILE)

# Send requests to Github API
responses = requestGithub(keywordsFile, args)
