CLEAN_TOKEN_STEP1 = '[\=;\\"\<\>]'
CLEAN_TOKEN_STEP2 = "[']"

def initTokensMap():
    tokensMap = {}
    tokensMap['AWS'] = '([^A-Z0-9]|^)(AKIA|A3T|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{12,}'
    tokensMap['FACEBOOK'] = '\W([0-9a-f]{32})$'
    tokensMap['GITHUB_CLIENT_SECRET'] = '[\W]{1,2}([a-f0-9]{40})[\W]{1,2}$'
    tokensMap['GOOGLE_SECRET'] = '\W([a-z0-9A-Z]{24})\W'
    tokensMap['GOOGLE_URL'] = '([0-9]{12}-[a-z0-9]{32}.apps.googleusercontent.com)'
    tokensMap['GOOGLE_OAUTH_ACCESS_TOKEN'] = '(ya29\\.[0-9A-Za-z\\-_]+)'
    tokensMap['HEROKU'] = '(?:HEROKU_API_KEY|HEROKU_API_TOKEN|HEROKU_API_SECRET|heroku_api_key|heroku_api_token|heroku_api_secret)[\W|\s]{1,}([0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})\W'
    tokensMap['MAILCHIMP'] = '\W([a-f0-9]{32}(-us2|-us3|-us4|-us5|-us6|-us7|-us8))\W'
    tokensMap['MAILGUN'] = '(key-[0-9a-f]{32})'
    tokensMap['PAYPAL'] = '[\W]{1,2}([E][A-Z]{1}[a-zA-Z0-9_-]{78})[\W]{1,2}$'
    tokensMap['PRIVATE_SSH_KEY'] = '(-----BEGIN PRIVATE KEY-----[a-zA-Z0-9\W].*-----END PRIVATE KEY-----)'
    tokensMap['SLACK'] = '\W(xox[p|b|o|a]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32})\W'
    tokensMap['SLACK_WEBHOOK_URL'] = '(hooks.slack.com\/services\/T[A-Z0-9]{8}\/B[A-Z0-9]{8}\/[a-zA-Z0-9]{1,})'
    tokensMap['SQUARE_APP_SECRET'] = 'sq0[a-z]{3}-[0-9A-Za-z\-_]{43}'
    tokensMap['SQUARE_PERSONAL_ACCESS_TOKEN'] = '\W(EAAA[a-zA-Z0-9_-]{60})\W'
    tokensMap['STRIPE_LIVE_SECRET_KEY'] = '(sk_live_[0-9a-zA-Z]{24})'
    tokensMap['STRIPE_LIVE_RESTRICTED_KEY'] = '(rk_live_[0-9a-zA-Z]{34})'
    tokensMap['TWITTER'] = '[\W]{1,2}([a-zA-Z0-9]{50})[\W]{1,2}$'
    return tokensMap
