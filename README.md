![gitgraberlogo](https://i.ibb.co/ry5K7Hv/logo-gitgraber.png)

<img src="https://img.shields.io/badge/made%20with-python-blue.svg" alt="made with python 3.x"> <img src="https://img.shields.io/github/issues/hisxo/gitgraber.svg">
# About gitGraber

**gitGraber is a tool developed in Python3 to monitor GitHub to search and find sensitive data in real time for different online services such as: Google, Amazon (AWS), Paypal, Github, Mailgun, Facebook, Twitter, Heroku, Stripe, Twilio...**

![demo](https://i.ibb.co/NS92P2y/preview-git-Graber-monitoring-github-real-time.png)

## How it works ?

It's important to understand that gitGraber is not designed to check history of repositories, many tools can already do that great. gitGraber was originally developed to monitor and parse last indexed files on GitHub. If gitGraber find something interesting, you will receive a notification on your Slack channel. You can also use it to have results directly on the command line.

In our experience, we are convinced that leaks do not come only from the organizations themselves, but also from service providers and employees, who do not necessarily have a "profile" indicating that they work for a particular organization.

Regex are supposed to be as accurate as possible. Sometimes, maybe you will have false-positive, feel free to contribute to improve recon and add new regex for pattern detection.

We prefer to reduce false positive instead of sending notification for every "standard" API keys which could found by gitGraber but irrelevant for your monitoring.

## Usage

``````````
usage: gitGraber.py [-h] [-k KEYWORDSFILE] [-q QUERY] [-s] [-w WORDLIST]

optional arguments:
  -h, --help                              Show this help message and exit
  -k KEYWORDSFILE, --keyword KEYWORDSFILE Specify a keywords file (-k keywordsfile.txt)
  -q QUERY, --query QUERY                 Specify your github query (-q "apikey")
  -s, --slack                             Enable slack notifications
  -w WORDLIST, --wordlist WORDLIST        Create a wordlist that fills dynamically with discovered filenames on GitHub
``````````
For example, to search for a specific word in github in combination with each word of the file keywordsfile.txt and output it to Slack  :

``````````
python3 gitGraber.py -k keywordsfile.txt -q YOURWORD -s
``````````
It is possible to search for a specific domain name for example, but this has to be surrounded by double quotes :

``````````
python3 gitGraber.py -k keywordsfile.txt -q \"yahoo.com\" -s
``````````

If you want to build a custom wordlist based on the files found on Github to use it then with your favorite fuzzing tool :


``````````
python3 gitGraber.py -k keywordsfile.txt -q \"yahoo.com\" -s -w mysuperwordlist.txt
``````````

## Dependencies

gitGraber needs some dependencies, to install them on your environment:

``pip3 install -r requirements.txt``

## Configuration

Before to start **gitGraber** you need to modify the configuration file ``config.py`` :

- Add your own Github tokens (_Personal access tokens_) : ``GITHUB_TOKENS = ['yourToken1Here','yourToken2Here']``
- Add your own Slack Webhook : ``SLACK_WEBHOOKURL = 'https://hooks.slack.com/services/TXXXX/BXXXX/XXXXXXX'``

| Service	| Link                                                                                                                  | 
|---------|-----------------------------------------------------------------------------------------------------------------------|
| GitHub  | *[How to create GitHub API token](https://github.com/settings/tokens)*                                                |
| Slack   | *[How to create Slack Webhook URL](https://get.slack.help/hc/en-us/articles/115005265063-Incoming-WebHooks-for-Slack)*|

To start gitGraber : ``python3 gitGraber.py -k wordlists/keywords.txt -q "uber" -s``

_We recommend creating a cron that will execute the script regulary_ :

``*/15 * * * * cd /BugBounty/gitGraber/ && /usr/bin/python3 gitGraber.py -k wordlists/keywords.txt -q "uber" -s >/dev/null 2>&1``

## Which API Keys & services are supported ? (Last update : September 12th, 2019)

Currently, gitGraber supports 31 different tokens. All of these detection models (regex) are stored in the file `` tokens.py`` :

- AWS
- FACEBOOK
- GITHUB_CLIENT_SECRET
- GOOGLE_SECRET
- GOOGLE_URL
- GOOGLE_FIREBASE_OR_MAPS
- GOOGLE_OAUTH_ACCESS_TOKEN
- HEROKU
- JSON_WEB_TOKEN
- MAILCHIMP
- MAILGUN
- PAYPAL
- PRIVATE_SSH_KEY
- PRIVATE_RSA_KEY
- PRIVATE_DSA_KEY
- PRIVATE_EC_KEY
- PRIVATE_PGP_KEY
- PRIVATE_OPENSSH_KEY
- SENDGRID_API_KEY
- SENSITIVE_URL
- SLACK_V2
- SLACK_V1
- SLACK_WEBHOOK_URL
- SQUARE_APP_SECRET
- SQUARE_PERSONAL_ACCESS_TOKEN
- STRIPE_LIVE_SECRET_KEY
- STRIPE_LIVE_RESTRICTED_KEY
- TWITTER
- TWILIO_AUTH
- TWILIO_SID
- TWILIO_API_KEY

## Wordlists & Resources

Some wordlists & regex have been created by us and some others are inspired from other repos/researchers :

* Link : https://gist.github.com/nullenc0de/fa23444ed574e7e978507178b50e1057
* Link : https://github.com/streaak/keyhacks
* Link : https://mathiasbynens.be/demo/url-regex

## TODO

- [X] Add a false positive detection
- [ ] Add args to only output results (to hide status code and other things)
- [X] Send only one notification for double tokens (for services like Twilio)
- [ ] Filter to send notification only if commit date is > to date defined in args
- [X] Improve "commit date" notification to display something like "[+] Commit date (5 days ago)"
- [ ] Add args to output results in file
- [ ] Add multi threads
- [ ] Improve token cleaning output
- [X] Add a "combo check" module (for services like Twilio that require two tokens)
- [X] Add user and org names display in notifications
- [X] Add commit date
- [X] Manage rate limit

# Authors

* Reptou - [Twitter : @R_Marot](https://twitter.com/R_Marot)
* Hisxo - [Twitter : @adrien_jeanneau](https://twitter.com/adrien_jeanneau)

# Contributors

_Thanks for your contribution and for your help to improve gitGraber:_

- [@Darkpills](https://github.com/hisxo/gitGraber/pulls?q=is%3Apr+author%3Adarkpills)

# Disclaimer

This project is made for educational and ethical testing purposes only. Usage of this tool for attacking targets without prior mutual consent is illegal. Developers assume no liability and are not responsible for any misuse or damage caused by this tool.
