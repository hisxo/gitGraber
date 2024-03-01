import os

# Configurable constants
GITHUB_TOKENS = ['X', 'X', 'X', 'X', 'X']
GITHUB_URL_FILE = 'rawGitUrls.txt'
GITHUB_API_URL = 'https://api.github.com/search/code?q='
GITHUB_API_COMMIT_URL = 'https://api.github.com/repos/'
GITHUB_SEARCH_PARAMS = '&sort=indexed&o=desc'
GITHUB_BASE_URL = 'https://github.com'
SLACK_WEBHOOKURL = 'https://hooks.slack.com/services/TXXXXXXXX/BXXXXXXXX/XXXXXXXXXXXXXXXXXXXXXXX'

# Ensure file path exists
def ensure_file_path(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

# Initialize file
def init_file(file_path):
    if not os.path.exists(file_path):
        ensure_file_path(file_path)
        with open(file_path, 'w'):
            pass

# Initialize URL file
def init_url_file():
    init_file(GITHUB_URL_FILE)

# Notify Slack
def notify_slack(message):
    if not SLACK_WEBHOOKURL:
        print('Please define Slack Webhook URL to enable notifications')
        return
    requests.post(SLACK_WEBHOOKURL, json={'text': ':new:' + message})

# Other functions remain unchanged...

# Main function
def main():
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
        init_file(args.wordlist)
    
    # Initialize URL file
    init_url_file()

    # Send requests to Github API
    responses = request_github(keywords_file, args)

if __name__ == "__main__":
    main()
