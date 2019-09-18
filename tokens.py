CLEAN_TOKEN_STEP1 = '[\=;\\"\<\>,)(]'
CLEAN_TOKEN_STEP2 = "[']"

def initTokensMap():
    tokensList = []
    tokensCombo = []
    tokensList.append(Token('AMAZON_AWS', '([^A-Z0-9]|^)(AKIA|A3T|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{12,}',['EXAMPLE']))
    tokensList.append(Token('FACEBOOK', '\W([0-9a-f]{32})$'))
    tokensList.append(Token('GITHUB_CLIENT_SECRET', '[\W]{1,2}([a-f0-9]{40})[\W]{1,2}$'))
    tokensList.append(Token('GOOGLE_FIREBASE_OR_MAPS', '(AIza[0-9A-Za-z\\-_]{35})'))
    tokensList.append(Token('GOOGLE_OAUTH_ACCESS_TOKEN', '(ya29\\.[0-9A-Za-z\\-_]+)'))
    tokensList.append(Token('HEROKU', '(?:HEROKU_API_KEY|HEROKU_API_TOKEN|HEROKU_API_SECRET|heroku_api_key|heroku_api_token|heroku_api_secret|heroku_key|HEROKU_TOKEN|HEROKU_AUTH|heroku_auth|herokuAuth|heroku_auth_token)[\W|\s]{1,}([0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})\W'))
#   tokensList.append(Token('JSON_WEB_TOKEN', '(eyJ[a-zA-Z0-9]{10,}\.eyJ[a-zA-Z0-9]{10,}\.[a-zA-Z0-9_-]{10,})'))
    tokensList.append(Token('MAILCHIMP', '\W(?:[a-f0-9]{32}(-us[0-9]{1,2}))\W'))
    tokensList.append(Token('MAILGUN', '(key-[0-9a-f]{32})'))
    tokensList.append(Token('PAYPAL', '[\W]{1,2}([E][A-Z]{1}[a-zA-Z0-9_-]{78})[\W]{1,2}$'))
    tokensList.append(Token('PRIVATE_SSH_KEY', '(-----BEGIN PRIVATE KEY-----[a-zA-Z0-9\S]{100,}-----END PRIVATE KEY-----)'))
    tokensList.append(Token('PRIVATE_RSA_KEY', '(-----BEGIN RSA PRIVATE KEY-----[a-zA-Z0-9\S]{100,}-----END RSA PRIVATE KEY-----)'))
    tokensList.append(Token('PRIVATE_DSA_KEY', '(-----BEGIN DSA PRIVATE KEY-----[a-zA-Z0-9\S]{100,}-----END DSA PRIVATE KEY-----)'))
    tokensList.append(Token('PRIVATE_EC_KEY', '(-----BEGIN EC PRIVATE KEY-----[a-zA-Z0-9\S]{100,}-----END EC PRIVATE KEY-----)'))
    tokensList.append(Token('PRIVATE_PGP_KEY', '(-----BEGIN PGP PRIVATE KEY BLOCK-----[a-zA-Z0-9\S]{100,}-----END PGP PRIVATE KEY BLOCK-----)'))
    tokensList.append(Token('PRIVATE_OPENSSH_KEY', '(-----BEGIN OPENSSH PRIVATE KEY-----[a-zA-Z0-9\S]{100,}-----END OPENSSH PRIVATE KEY-----)'))
    tokensList.append(Token('SENDGRID_API_KEY', '(SG\.[a-zA-Z0-9-_]{22}\.[a-zA-Z0-9_-]{43})'))
    tokensList.append(Token('SENSITIVE_URL', '\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))'))
    tokensList.append(Token('SLACK_V2', '\W(xox[p|b|o|a]-[0-9]{1,}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32})\W'))
    tokensList.append(Token('SLACK_V1', '\W(xox[p|b|o|a]-[0-9]{1,}-[0-9]{1,}-[a-zA-Z0-9]{24})\W'))
    tokensList.append(Token('SLACK_WEBHOOK_URL', '(hooks.slack.com\/services\/T[A-Z0-9]{8}\/B[A-Z0-9]{8}\/[a-zA-Z0-9]{1,})',['0000','XXXX']))
    tokensList.append(Token('SQUARE_APP_SECRET', 'sq0[a-z]{3}-[0-9A-Za-z\-_]{43}'))
    tokensList.append(Token('SQUARE_PERSONAL_ACCESS_TOKEN', '\W(EAAA[a-zA-Z0-9_-]{60})\W'))
    tokensList.append(Token('STRIPE_LIVE_SECRET_KEY', '(sk_live_[0-9a-zA-Z]{24})'))
    tokensList.append(Token('STRIPE_LIVE_RESTRICTED_KEY', '(rk_live_[0-9a-zA-Z]{24,34})'))
    tokensList.append(Token('TWITTER', '[\W]{1,2}([a-zA-Z0-9]{50})[\W]{1,2}$'))
    tokensList.append(Token('TWILIO_API_KEY', 'SK[0-9a-fA-F]{32}'))

## Tokens which need two keys to be interesting ##

    googleSecret = Token('GOOGLE_SECRET', r'(\'|\"|\=)(?=(.*[0-9].*))(?=(.*[A-Z].*))(?=([0-9A-Za-z-_]{24})(\1|\'|\"|(\s*(\r\n|\r|\n))))(?!.*\1.*\1.*)(?=(.*[a-z].*))(.*)(\1|\'|\"|(\s*(\r\n|\r|\n)))', None, 2)
    googleUrl = Token('GOOGLE_URL', '([0-9]{12}-[a-z0-9]{32}.apps.googleusercontent.com)', None, 1)
    tokensCombo.append(TokenCombo('GOOGLE', [googleSecret, googleUrl]))

    twilioSID = Token('TWILIO_SID', '(AC[a-f0-9]{32}[^a-f0-9])', None, 1)
    twilioAUTH = Token('TWILIO_AUTH', '\W[a-f0-9]{32}\W', None, 2)
    tokensCombo.append(TokenCombo('TWILIO', [twilioSID, twilioAUTH]))
 
    return tokensList, tokensCombo

class Token:

    def __init__(self, name, regex, blacklist = [], displayOrder = 1):
        self.name = name
        self.regex = regex
        self.blacklist = blacklist
        self.displayOrder = displayOrder
    
    def getName(self):
        return self.name
    
    def getRegex(self):
        return self.regex

    def getBlacklist(self):
        return self.blacklist

    def getDisplayOrder(self):
        return self.displayOrder

class TokenCombo:

    def __init__(self, name, tokensList = []):
        self.tokensList = tokensList
        self.name = name
    
    def getTokens(self):
        return self.tokensList
    
    def getName(self):
        return self.name


