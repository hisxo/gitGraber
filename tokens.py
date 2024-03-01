import re

def clean_tokens(tokens):
    """
    Cleans tokens by removing unwanted characters.
    """
    cleaned_tokens = []
    for token in tokens:
        cleaned_token = re.sub(r"[\=;\\"\<\>']", '', token)
        cleaned_tokens.append(cleaned_token)
    return cleaned_tokens

def init_tokens_map():
    tokens_map = {
        'AWS': r'([^A-Z0-9]|^)(AKIA|A3T|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{12,}',
        'FACEBOOK': r'\W([0-9a-f]{32})$',
        'GITHUB_CLIENT_SECRET': r'[\W]{1,2}([a-f0-9]{40})[\W]{1,2}$',
        'GOOGLE_SECRET': r'\W([a-z0-9A-Z]{24})\W',
        'GOOGLE_URL': r'([0-9]{12}-[a-z0-9]{32}.apps.googleusercontent.com)',
        'GOOGLE_OAUTH_ACCESS_TOKEN': r'(ya29\\.[0-9A-Za-z\\-_]+)',
        'HEROKU': r'(?:HEROKU_API_KEY|HEROKU_API_TOKEN|HEROKU_API_SECRET|heroku_api_key|heroku_api_token|heroku_api_secret)[\W|\s]{1,}([0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})\W',
        'MAILCHIMP': r'\W(?:[a-f0-9]{32}(-us[0-9]{1,2}))\W',
        'MAILGUN': r'(key-[0-9a-f]{32})',
        'PAYPAL': r'[\W]{1,2}([E][A-Z]{1}[a-zA-Z0-9_-]{78})[\W]{1,2}$',
        'PRIVATE_SSH_KEY': r'(-----BEGIN PRIVATE KEY-----[a-zA-Z0-9\W].*-----END PRIVATE KEY-----)',
        'PRIVATE_RSA_KEY': r'(-----BEGIN RSA PRIVATE KEY-----[a-zA-Z0-9\W].*-----END RSA PRIVATE KEY-----)',
        'PRIVATE_DSA_KEY': r'(-----BEGIN DSA PRIVATE KEY-----[a-zA-Z0-9\W].*-----END DSA PRIVATE KEY-----)',	
        'PRIVATE_EC_KEY': r'(-----BEGIN EC PRIVATE KEY-----[a-zA-Z0-9\W].*-----END EC PRIVATE KEY-----)',
        'PRIVATE_PGP_KEY': r'(-----BEGIN PGP PRIVATE KEY BLOCK-----[a-zA-Z0-9\W].*-----END PGP PRIVATE KEY BLOCK-----)',
        'PRIVATE_OPENSSH_KEY': r'(-----BEGIN OPENSSH PRIVATE KEY-----[a-zA-Z0-9\W].*-----END OPENSSH PRIVATE KEY-----)',
        'SENDGRID_API_KEY': r'(SG\.[a-zA-Z0-9-_]{22}\.[a-zA-Z0-9_-]{43})',
        'SLACK_V2': r'\W(xox[p|b|o|a]-[0-9]{1,}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32})\W',
        'SLACK_V1': r'\W(xox[p|b|o|a]-[0-9]{1,}-[0-9]{1,}-[a-zA-Z0-9]{24})\W',
        'SLACK_WEBHOOK_URL': r'(hooks.slack.com\/services\/T[A-Z0-9]{8}\/B[A-Z0-9]{8}\/[a-zA-Z0-9]{1,})',
        'SQUARE_APP_SECRET': r'sq0[a-z]{3}-[0-9A-Za-z\-_]{43}',
        'SQUARE_PERSONAL_ACCESS_TOKEN': r'\W(EAAA[a-zA-Z0-9_-]{60})\W',
        'STRIPE_LIVE_SECRET_KEY': r'(sk_live_[0-9a-zA-Z]{24})',
        'STRIPE_LIVE_RESTRICTED_KEY': r'(rk_live_[0-9a-zA-Z]{24,34})',
        'TWITTER': r'[\W]{1,2}([a-zA-Z0-9]{50})[\W]{1,2}$'
    }
    return tokens_map

if __name__ == "__main__":
    tokens_map = init_tokens_map()
    print(tokens_map)
