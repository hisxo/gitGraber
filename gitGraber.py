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
import urllib.parse
from functools import partial
from datetime import datetime
from pprint import pprint
from termcolor import colored
from urllib.parse import urlparse
from multiprocessing.dummy import Pool
from crontab import CronTab

def getFilenameForQuery(query):
    if query:
        query_name = query.replace(" ", "_")
        return f'rawGitUrls_{query_name}.txt'
    else:
        return 'rawGitUrls.txt'

def createEmptyBinaryFile(name):
    f = open(name, 'wb')
    f.write(1*b'\0')
    f.close()

def initFile(name):
    if not os.path.exists(name) or os.path.getsize(name) == 0:
        with open(name, 'wb') as f:
            f.write(b'\0')

    f = open(name, 'a+')
    
    # Check if the file is empty
    if f.tell() == 0:
        f.write("Initialized\n")
        f.flush()  # Ensure the content is written to the file
    
    f.close()

def clean(result):
    cleanToken = re.sub(tokens.CLEAN_TOKEN_STEP1, '', result.group(0))
    return re.sub(tokens.CLEAN_TOKEN_STEP2, '', cleanToken)

def monitor():
    cmd='/usr/bin/python3 '+str(path_script)+'/gitGraber.py -q "'+args.query+'"'
    my_cron = CronTab(user=True)
    if args.discord and config.DISCORD_WEBHOOKURL:
        if(args.wordlist):
            job = my_cron.new(command=cmd+' -d -k '+args.keywordsFile+' -w '+args.wordlist+'')
            job.minute.every(30)
            my_cron.write() 
        else:
            job = my_cron.new(command=cmd+' -d -k '+args.keywordsFile+'')
            job.minute.every(30)
            my_cron.write() 
    elif args.slack and config.SLACK_WEBHOOKURL:
        if(args.wordlist):
            job = my_cron.new(command=cmd+' -s -k '+args.keywordsFile+' -w '+args.wordlist+'')
            job.minute.every(30)
            my_cron.write() 
        else:
            job = my_cron.new(command=cmd+' -s -k '+args.keywordsFile+'')
            job.minute.every(30)
            my_cron.write() 
    elif args.telegram and (config.TELEGRAM_CONFIG or config.TELEGRAM_CONFIG.get("token") or config.TELEGRAM_CONFIG.get("chat_id")):
        if(args.wordlist):
            job = my_cron.new(command=cmd+' -tg -k '+args.keywordsFile+' -w '+args.wordlist+'')
            job.minute.every(30)
            my_cron.write() 
        else:
            job = my_cron.new(command=cmd+' -tg -k '+args.keywordsFile+'')
            job.minute.every(30)
            my_cron.write() 

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

def notify(platform, message):
    if platform == "discord":
        if not config.DISCORD_WEBHOOKURL:
            print('Please define Discord Webhook URL to enable notifications')
            exit()
        data = {'content': message}
        headers = {"Content-Type": "application/json"}
        requests.post(config.DISCORD_WEBHOOKURL, data=json.dumps(data), headers=headers)

    elif platform == "slack":
        if not config.SLACK_WEBHOOKURL:
            print('Please define Slack Webhook URL to enable notifications')
            exit()
        requests.post(config.SLACK_WEBHOOKURL, json={'text': ':new:' + message})

    elif platform == "telegram":
        if not config.TELEGRAM_CONFIG or not config.TELEGRAM_CONFIG.get("token") or not config.TELEGRAM_CONFIG.get("chat_id"):
            print('Please define Telegram config to enable notifications')
            exit()
        telegramUrl = "https://api.telegram.org/bot{}/sendMessage".format(config.TELEGRAM_CONFIG.get("token"))
        requests.post(telegramUrl, json={'text': message, 'chat_id': config.TELEGRAM_CONFIG.get("chat_id")})

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
    if urlInfos[5]:
        orgString = '[+] User Organizations : '+','.join(urlInfos[5])
        print(orgString)
        orgString = '\n'+orgString
    else:
        orgString = ''
    return possibleTokenString+'\n'+commitString+'\n'+urlString+'\n'+tokenString+'\n'+repoString+orgString

def parseResults(content, limit_days=None):
    data = json.loads(content)
    contentRaw = {}
    f = open(config.GITHUB_URL_FILE, 'a+', encoding='utf-8')
    try:
        for item in data['items']:
            gitUrl = item['url']
            repoName = item['repository']['full_name']
            orgUrl = item['repository']['owner']['organizations_url']
            #Parse JSON to get info about repository
            response = doRequestGitHub(gitUrl)
            rawUrl = json.loads(response.text)
            rawGitUrl = rawUrl['download_url']
          
            #Parse JSON to get info about organizations
            if orgUrl not in checkedOrgs.keys():
                checkedOrgs[orgUrl] = []
                response = doRequestGitHub(orgUrl, True)
                orgData = json.loads(response.text)
                for org in orgData:
                    checkedOrgs[orgUrl].append(org['login'])
            
            #Request to extract data about repository and user
            commitHash = gitUrl.split('ref=')[1]
            commitUrl = config.GITHUB_API_COMMIT_URL+repoName+'/commits/'+commitHash
            response = doRequestGitHub(commitUrl, True)
            commitData = json.loads(response.text)
            commitDate = commitData['commit']['author']['date']
            
            #Compare the current date and date of commit
            currentTimestamp = int(time.time())
            timestampCommit = int(time.mktime(datetime.strptime(commitDate, '%Y-%m-%dT%H:%M:%SZ').timetuple()))
            compareCommitDate = (currentTimestamp - timestampCommit)/3600
           
            # Check if the commit is within the user-specified limit
            if limit_days is not None and compareCommitDate > limit_days * 24:
                continue

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
               contentRaw[rawGitUrl].append(checkedOrgs[orgUrl])
        return contentRaw

    except Exception as e:
        print('Exception '+str(e))
        pass

# Transform the config github token list to a dict of key values
def initGithubToken():
    return [{"token": token, "remaining": 1, "reset": time.time()} for token in config.GITHUB_TOKENS]

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

def doRequestGitHub(url, authd=True, verbose=False):
    nbMaxTry = config.GITHUB_MAX_RETRY
    while nbMaxTry > 0:
        if verbose:
            print(colored('[i] Github query : ' + url, 'yellow'))
        headers = {
            'Accept': 'application/vnd.github.v3.text-match+json'
        }
        if authd:
            token = getGithubToken(url)
            headers['Authorization'] = 'token '+ token
        try:
            response = requests.get(url, headers=headers)
            nbMaxTry = nbMaxTry - 1
            if verbose:
                print('[i] Status code : ' + str(response.status_code))
            if authd:
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
            print(colored("%s" % e.msg), 'red')
            pass
        
        except requests.exceptions.ConnectionError as e:
            print(colored('Connection to Github failed', 'red'))
            pass

def doSearchGithub(args,tokenMap, tokenCombos,keyword):
    url = config.GITHUB_API_URL + urllib.parse.quote(githubQuery +' '+keyword.strip()) +config.GITHUB_SEARCH_PARAMS
    print(url)
    response = doRequestGitHub(url, True, True)
    if response:
        content = parseResults(response.text, args.limit_days)
        if content:
            for rawGitUrl in content.keys():
                tokensResult = checkToken(content[rawGitUrl][0].text, tokenMap, tokenCombos)
                for token in tokensResult.keys():
                    displayMessage = displayResults(token, tokensResult, rawGitUrl, content[rawGitUrl])
                    if args.discord:
                        notify("discord", displayMessage)
                    if args.slack:
                        notify("slack", displayMessage)
                    if args.telegram:
                        notify("telegram", displayMessage)
                    if args.wordlist:
                        writeToWordlist(rawGitUrl, args.wordlist)

def searchGithub(keywordsFile, args):
    tokenMap, tokenCombos = tokens.initTokensMap()

    t_keywords = open(keywordsFile).read().split("\n")

    pool = Pool( int(args.max_threads) )
    pool.map( partial(doSearchGithub,args,tokenMap, tokenCombos), t_keywords )
    pool.close()
    pool.join()


parser = argparse.ArgumentParser()
argcomplete.autocomplete(parser)
parser.add_argument('-t', '--threads', action='store', dest='max_threads', help='Max threads to speed the requests on Github (take care about the rate limit)', default="3")
parser.add_argument('-k', '--keyword', action='store', dest='keywordsFile', help='Specify a keywords file (-k keywordsfile.txt)', default="wordlists/keywords.txt")
parser.add_argument('-q', '--query', action='store', dest='query', help='Specify your query (-q "myorg")')
parser.add_argument('-d', '--discord', action='store_true', help='Enable discord notifications', default=False)
parser.add_argument('-s', '--slack', action='store_true', help='Enable slack notifications', default=False)
parser.add_argument('-tg', '--telegram', action='store_true', help='Enable telegram notifications', default=False)
parser.add_argument('-m', '--monitor', action='store_true', help='Monitors your query by adding a cron job for every 30 mins',default=False)
parser.add_argument('-w', '--wordlist', action='store', dest='wordlist', help='Create a wordlist that fills dynamically with discovered filenames on GitHub')
parser.add_argument('-l', '--limit', action='store', dest='limit_days', type=int, help='Limit the results to commits less than N days old', default=None)
args = parser.parse_args()

if not args.query or args.query == "":
    print('No query (-q or --query) is specified, default query will be used')
    args.query = ' '
    githubQuery = args.query

keywordsFile = args.keywordsFile
githubQuery = args.query
path_script=os.path.dirname(os.path.realpath(__file__))
config.GITHUB_TOKENS_STATES = {}
checkedOrgs = {}

# If wordlist, check if file is binary initialized for mmap 
if(args.wordlist):
    initFile(args.wordlist)
# If monitor, create crontab for every 15 mins by default
if (args.monitor):
    monitor()
else:
    pass

# Init URL file 
config.GITHUB_URL_FILE = getFilenameForQuery(args.query)
initFile(config.GITHUB_URL_FILE)

# Send requests to Github API
responses = searchGithub(keywordsFile, args)
