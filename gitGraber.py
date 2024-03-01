import os
import re
import mmap
import json
import argparse
import requests
import argcomplete
from termcolor import colored

import config
import tokens

def create_empty_binary_file(name):
    with open(name, 'wb') as f:
        f.write(1 * b'\0')

def init_file(name):
    if not name or os.path.getsize(name) == 0:
        create_empty_binary_file(name)

def check_token(content, tokens_map):
    tokens = {}
    for token_type, regex_pattern in tokens_map.items():
        match = re.search(regex_pattern, content)
        if match:
            tokens[match.group(0)] = token_type
    return tokens

def notify_slack(message):
    if not config.SLACK_WEBHOOKURL:
        print('Please define Slack Webhook URL to enable notifications')
        return
    requests.post(config.SLACK_WEBHOOKURL, json={'text': ':new:' + message})

def write_to_wordlist(content, wordlist):
    with open(wordlist, 'a+') as f:
        s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        filename = content.split('/')[-1]
        if s.find(bytes(filename, 'utf-8')) == -1:
            f.write(filename + '\n')

def display_results(result, token_result, raw_git_url, url_infos):
    possible_token_string = '[!] POSSIBLE ' + token_result[result] + \
                            ' TOKEN FOUND (keyword used:' + github_query + ')'
    print(colored(possible_token_string, 'green'))
    commit_string = '[+] Commit date : ' + url_infos[2] + ' by ' + url_infos[3]
    print(commit_string)
    url_string = '[+] RAW URL : ' + raw_git_url
    print(url_string)
    clean_token = re.sub(tokens.CLEAN_TOKEN_STEP1, '', result.group(0))
    clean_token = re.sub(tokens.CLEAN_TOKEN_STEP2, '', clean_token)
    token_string = '[+] Token : ' + clean_token
    print(token_string.strip())
    repo_string = '[+] Repository URL : ' + url_infos[1]
    print(repo_string)
    return possible_token_string + '\n' + commit_string + '\n' + url_string + '\n' + token_string + '\n' + repo_string

def parse_results(content):
    try:
        data = json.loads(content)
        content_raw = {}
        with open(config.GITHUB_URL_FILE, 'a+', encoding='utf-8') as f:
            for item in data['items']:
                git_url = item['url']
                repo_name = item['repository']['full_name']
                commit_hash = git_url.split('ref=')[1]
                commit_url = config.GITHUB_API_COMMIT_URL + repo_name + '/commits/' + commit_hash

                headers = {'Accept': 'application/vnd.github.v3.text-match+json',
                           'Authorization': 'token ' + config.GITHUB_TOKENS[3]}
                response = requests.get(git_url, headers=headers)
                raw_url = json.loads(response.text)
                raw_git_url = raw_url['download_url']

                response = requests.get(commit_url, headers=headers)
                commit_data = json.loads(response.text)
                commit_date = commit_data['commit']['author']['date']
                commit_author = commit_data['commit']['author']['email']

                s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
                if s.find(bytes(raw_git_url, 'utf-8')) == -1:
                    f.write(raw_git_url + '\n')
                    content_raw[raw_git_url] = []
                    content_raw[raw_git_url].append(requests.get(raw_git_url, headers=headers))
                    content_raw[raw_git_url].append(config.GITHUB_BASE_URL + '/' + repo_name)
                    content_raw[raw_git_url].append(commit_date)
                    content_raw[raw_git_url].append(commit_author)
        return content_raw
    except KeyError:
        print(colored('[!] Github API rate-limit detected, please retry with other tokens', 'red'))
        return {}
    except Exception as e:
        print('Exception: ' + str(e))
        return {}

def request_github(keywords_file, args):
    keyword_searches = []
    token_map = tokens.init_tokens_map()
    with open(keywords_file, 'r') as myfile:
        for keyword in myfile:
            for token in config.GITHUB_TOKENS:
                print(colored('[+] Github query : ' + config.GITHUB_API_URL + github_query + ' ' + keyword.strip() +
                              config.GITHUB_SEARCH_PARAMS, 'yellow'))
                headers = {'Accept': 'application/vnd.github.v3.text-match+json',
                           'Authorization': 'token ' + token}
                try:
                    response = requests.get(
                        config.GITHUB_API_URL + github_query + ' ' + keyword.strip() + config.GITHUB_SEARCH_PARAMS,
                        headers=headers)
                    print('[i] Status code : ' + str(response.status_code))
                    if response.status_code == 200:
                        content = parse_results(response.text)
                        if content:
                            for raw_git_url in content.keys():
                                tokens_result = check_token(content[raw_git_url][0].text, token_map)
                                for token in tokens_result.keys():
                                    display_message = display_results(token, tokens_result, raw_git_url,
                                                                      content[raw_git_url])
                                    if args.slack:
                                        notify_slack(display_message)
                                    if args.wordlist:
                                        write_to_wordlist(raw_git_url, args.wordlist)
                        break
                except UnicodeEncodeError as e:
                    print(e)
                    pass
    return keyword_searches

parser = argparse.ArgumentParser()
argcomplete.autocomplete(parser)
parser.add_argument('-k', '--keyword', action='store', dest='keywords_file',
                    help='Specify a keywords file (-k keywordsfile.txt)')
parser.add_argument('-q', '--query', action='store', dest='query', help='Specify your query (-q "myorg")')
parser.add_argument('-s', '--slack', action='store_true', help='Enable slack notifications', default=False)
parser.add_argument('-w', '--wordlist', action='store', dest='wordlist',
                    help='Create a wordlist that fills dynamically with discovered filenames on GitHub')
args = parser.parse_args()

if not args.keywords_file:
    print('No keyword (-k or --keyword) file is specified')
    exit()

if not args.query:
    print('No query (-q or --query) is specified, default query will be used')
    args.query = ' '
    github_query = args.query

keywords_file = args.keywords_file
github_query = args.query
tokens_result = []

if args.wordlist:
    init_file
