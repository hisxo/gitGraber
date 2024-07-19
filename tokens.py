CLEAN_TOKEN_STEP1 = '[\=;\\"\<\>,)(]'
CLEAN_TOKEN_STEP2 = "[']"

def initTokensMap():
    tokensList = []
    tokensCombo = []
    tokensList.append(Token('APR1 MD5', '\\$apr1\\$[a-zA-Z0-9_/\\.]{8}\\$[a-zA-Z0-9_/\\.]{22}', []))
    tokensList.append(Token('APACHE SHA', '\\{SHA\\}[0-9a-zA-Z/_=]{10,}', []))
    tokensList.append(Token('BLOWFISH', '\\$2[abxyz]?\\$[0-9]{2}\\$[a-zA-Z0-9_/\\.]*', []))
    tokensList.append(Token('DRUPAL', '\\$S\\$[a-zA-Z0-9_/\\.]{52}', []))
    tokensList.append(Token('JOOMLAVBULLETIN', '[0-9a-zA-Z]{32}:[a-zA-Z0-9_]{16,32}', []))
    tokensList.append(Token('LINUX MD5', '\\$1\\$[a-zA-Z0-9_/\\.]{8}\\$[a-zA-Z0-9_/\\.]{22}', []))
    tokensList.append(Token('PHPBB3', '\\$H\\$[a-zA-Z0-9_/\\.]{31}', []))
    tokensList.append(Token('SHA512CRYPT', '\\$6\\$[a-zA-Z0-9_/\\.]{16}\\$[a-zA-Z0-9_/\\.]{86}', []))
    tokensList.append(Token('WORDPRESS', '\\$P\\$[a-zA-Z0-9_/\\.]{31}', []))
    tokensList.append(Token('SHA512', '(^|[^a-zA-Z0-9])[a-fA-F0-9]{128}([^a-zA-Z0-9]|$)', []))
    tokensList.append(Token('ADOBE CLIENT ID (OAUTH WEB)', '(adobe[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-f0-9]{32})[\'"]', []))
    tokensList.append(Token('ABODE CLIENT SECRET', '(p8e-)[a-z0-9]{32}', []))
    tokensList.append(Token('AGE SECRET KEY', 'AGE-SECRET-KEY-1[QPZRY9X8GF2TVDW0S3JN54KHCE6MUA7L]{58}', []))
    tokensList.append(Token('ALCHEMI API KEY', '(alchemi[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-zA-Z0-9-]{32})[\'"]', []))
    tokensList.append(Token('ALIBABA ACCESS KEY ID', '(LTAI)[a-z0-9]{20}', []))
    tokensList.append(Token('ALIBABA SECRET KEY', '(alibaba[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-z0-9]{30})[\'"]', []))
    tokensList.append(Token('ARTIFACTORY API KEY & PASSWORD', '["\']AKC[a-zA-Z0-9]{10,}["\']|["\']AP[0-9ABCDEF][a-zA-Z0-9]{8,}["\']', []))
    tokensList.append(Token('ASANA CLIENT ID', '((asana[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([0-9]{16})[\'"])|((asana[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-z0-9]{32})[\'"])', []))
    tokensList.append(Token('ATLASSIAN API KEY', '(atlassian[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-z0-9]{24})[\'"]', []))
    tokensList.append(Token('AWS CLIENT ID', '(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}', []))
    tokensList.append(Token('AWS MWS KEY', 'amzn\\.mws\\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', []))
    tokensList.append(Token('AWS SECRET KEY', 'aws(.{0,20})?[\'"][0-9a-zA-Z\\/+]{40}[\'"]', []))
    tokensList.append(Token('AWS APPSYNC GRAPHQL KEY', 'da2-[a-z0-9]{26}', []))
    tokensList.append(Token('BASIC AUTH CREDENTIALS', '://[a-zA-Z0-9]+:[a-zA-Z0-9]+@[a-zA-Z0-9]+\\.[a-zA-Z]+', []))
    tokensList.append(Token('BEAMER CLIENT SECRET', '(beamer[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"](b_[a-z0-9=_\\-]{44})[\'"]', []))
    tokensList.append(Token('BINANCE API KEY', '(binance[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-zA-Z0-9]{64})[\'"]', []))
    tokensList.append(Token('BITBUCKET CLIENT ID', '((bitbucket[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-z0-9]{32})[\'"])', []))
    tokensList.append(Token('BITBUCKET CLIENT SECRET', '((bitbucket[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-z0-9_\\-]{64})[\'"])', []))
    tokensList.append(Token('BITCOINAVERAGE API KEY', '(bitcoin.?average[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-zA-Z0-9]{43})[\'"]', []))
    tokensList.append(Token('BITQUERY API KEY', '(bitquery[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([A-Za-z0-9]{32})[\'"]', []))
    tokensList.append(Token('BIRISE API KEY', '(bitrise[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-zA-Z0-9_\\-]{86})[\'"]', []))
    tokensList.append(Token('BLOCK API KEY', '(block[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4})[\'"]', []))
    tokensList.append(Token('BLOCKCHAIN API KEY', 'mainnet[a-zA-Z0-9]{32}|testnet[a-zA-Z0-9]{32}|ipfs[a-zA-Z0-9]{32}', []))
    tokensList.append(Token('BLOCKFROST API KEY', '(blockchain[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[0-9a-f]{12})[\'"]', []))
    tokensList.append(Token('BOX API KEY', '(box[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-zA-Z0-9]{32})[\'"]', []))
    tokensList.append(Token('BRAVENEWCOIN API KEY', '(bravenewcoin[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-z0-9]{50})[\'"]', []))
    tokensList.append(Token('CLEARBIT API KEY', 'sk_[a-z0-9]{32}', []))
    tokensList.append(Token('CLOJARS API KEY', '(CLOJARS_)[a-zA-Z0-9]{60}', []))
    tokensList.append(Token('CLOUDINARY BASIC AUTH', 'cloudinary://[0-9]{15}:[0-9A-Za-z]+@[a-z]+', []))
    tokensList.append(Token('COINLAYER API KEY', '(coinlayer[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-z0-9]{32})[\'"]', []))
    tokensList.append(Token('COINLIB API KEY', '(coinlib[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-z0-9]{16})[\'"]', []))
    tokensList.append(Token('CONTENTFUL DELIVERY API KEY', '(contentful[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-z0-9=_\\-]{43})[\'"]', []))
    tokensList.append(Token('COVALENT API KEY', 'ckey_[a-z0-9]{27}', []))
    tokensList.append(Token('CHARITY SEARCH API KEY', '(charity.?search[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-z0-9]{32})[\'"]', []))
    tokensList.append(Token('DATABRICKS API KEY', 'dapi[a-h0-9]{32}', []))
    tokensList.append(Token('DDOWNLOAD API KEY', '(ddownload[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-z0-9]{22})[\'"]', []))
    tokensList.append(Token('DEFINED NETWORKING API TOKEN', '(dnkey-[a-z0-9=_\\-]{26}-[a-z0-9=_\\-]{52})', []))
    tokensList.append(Token('DISCORD API KEY, CLIENT ID & CLIENT SECRET', '((discord[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-h0-9]{64}|[0-9]{18}|[a-z0-9=_\\-]{32})[\'"])', []))
    tokensList.append(Token('DROPBOX API KEY', 'sl.[a-zA-Z0-9_-]{136}', []))
    tokensList.append(Token('DOPPLER API KEY', '(dp\\.pt\\.)[a-zA-Z0-9]{43}', []))
    tokensList.append(Token('DROPBOX API SECRET/KEY, SHORT & LONG LIVED API KEY', '(dropbox[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-z0-9]{15}|sl\\.[a-z0-9=_\\-]{135}|[a-z0-9]{11}(AAAAAAAAAA)[a-z0-9_=\\-]{43})[\'"]', []))
    tokensList.append(Token('DUFFEL API KEY', 'duffel_(test|live)_[a-zA-Z0-9_-]{43}', []))
    tokensList.append(Token('DYNATRACE API KEY', 'dt0c01\\.[a-zA-Z0-9]{24}\\.[a-z0-9]{64}', []))
    tokensList.append(Token('EASYPOST API KEY', 'EZAK[a-zA-Z0-9]{54}', []))
    tokensList.append(Token('EASYPOST TEST API KEY', 'EZTK[a-zA-Z0-9]{54}', []))
    tokensList.append(Token('ETHERSCAN API KEY', '(etherscan[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([A-Z0-9]{34})[\'"]', []))
    tokensList.append(Token('FACEBOOK ACCESS TOKEN', 'EAACEdEose0cBA[0-9A-Za-z]+', []))
    tokensList.append(Token('FACEBOOK CLIENT ID', '([fF][aA][cC][eE][bB][oO][oO][kK]|[fF][bB])(.{0,20})?[\'"][0-9]{13,17}', []))
    tokensList.append(Token('FACEBOOK OAUTH', '[fF][aA][cC][eE][bB][oO][oO][kK].*[\'|"][0-9a-f]{32}[\'|"]', []))
    tokensList.append(Token('FACEBOOK SECRET KEY', '([fF][aA][cC][eE][bB][oO][oO][kK]|[fF][bB])(.{0,20})?[\'"][0-9a-f]{32}', []))
    tokensList.append(Token('FASTLY API KEY', '(fastly[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-z0-9=_\\-]{32})[\'"]', []))
    tokensList.append(Token('FINICITY API KEY & CLIENT SECRET', '(finicity[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-f0-9]{32}|[a-z0-9]{20})[\'"]', []))
    tokensList.append(Token('FLUTTERWEAVE KEYS', 'FLWPUBK_TEST-[a-hA-H0-9]{32}-X|FLWSECK_TEST-[a-hA-H0-9]{32}-X|FLWSECK_TEST[a-hA-H0-9]{12}', []))
    tokensList.append(Token('FRAME.IO API KEY', 'fio-u-[a-zA-Z0-9_=\\-]{64}', []))
    tokensList.append(Token('GITHUB', 'github(.{0,20})?[\'"][0-9a-zA-Z]{35,40}', []))
    tokensList.append(Token('GITHUB APP TOKEN', '(ghu|ghs)_[0-9a-zA-Z]{36}', []))
    tokensList.append(Token('GITHUB OAUTH ACCESS TOKEN', 'gho_[0-9a-zA-Z]{36}', []))
    tokensList.append(Token('GITHUB PERSONAL ACCESS TOKEN', 'ghp_[0-9a-zA-Z]{36}', []))
    tokensList.append(Token('GITHUB REFRESH TOKEN', 'ghr_[0-9a-zA-Z]{76}', []))
    tokensList.append(Token('GITHUB FINE-GRAINED PERSONAL ACCESS TOKEN', 'github_pat_[0-9a-zA-Z_]{82}', []))
    tokensList.append(Token('GITLAB PERSONAL ACCESS TOKEN', 'glpat-[0-9a-zA-Z\\-]{20}', []))
    tokensList.append(Token('GITLAB PIPELINE TRIGGER TOKEN', 'glptt-[0-9a-f]{40}', []))
    tokensList.append(Token('GITLAB RUNNER REGISTRATION TOKEN', 'GR1348941[0-9a-zA-Z_\\-]{20}', []))
    tokensList.append(Token('GOCARDLESS API KEY', 'live_[a-zA-Z0-9_=\\-]{40}', []))
    tokensList.append(Token('GOFILE API KEY', '(gofile[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-zA-Z0-9]{32})[\'"]', []))
    tokensList.append(Token('GOOGLE API KEY', 'AIza[0-9A-Za-z_\\-]{35}', []))
    tokensList.append(Token('GOOGLE CLOUD PLATFORM API KEY', '(google|gcp|youtube|drive|yt)(.{0,20})?[\'"][AIza[0-9a-z_\\-]{35}][\'"]', []))
    tokensList.append(Token('GOOGLE DRIVE OAUTH', '[0-9]+-[0-9A-Za-z_]{32}\\.apps\\.googleusercontent\\.com', []))
    tokensList.append(Token('GOOGLE OAUTH ACCESS TOKEN', 'ya29\\.[0-9A-Za-z_\\-]+', []))
    tokensList.append(Token('GOOGLE (GCP) SERVICE-ACCOUNT', '"type.+:.+"service_account', []))
    tokensList.append(Token('GRAFANA API KEY', 'eyJrIjoi[a-z0-9_=\\-]{72,92}', []))
    tokensList.append(Token('GRAFANA CLOUD API TOKEN', 'glc_[A-Za-z0-9\\+/]{32,}={0,2}', []))
    tokensList.append(Token('GRAFANA SERVICE ACCOUNT TOKEN', '(glsa_[A-Za-z0-9]{32}_[A-Fa-f0-9]{8})', []))
    tokensList.append(Token('HASHICORP TERRAFORM USER/ORG API KEY', '[a-z0-9]{14}\\.atlasv1\\.[a-z0-9_=\\-]{60,70}', []))
    tokensList.append(Token('HEROKU API KEY', '[hH][eE][rR][oO][kK][uU].{0,30}[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}', []))
    tokensList.append(Token('HUBSPOT API KEY', '[\'"][a-h0-9]{8}-[a-h0-9]{4}-[a-h0-9]{4}-[a-h0-9]{4}-[a-h0-9]{12}[\'"]', []))
    tokensList.append(Token('INSTATUS API KEY', '(instatus[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-z0-9]{32})[\'"]', []))
    tokensList.append(Token('INTERCOM API KEY & CLIENT SECRET/ID', '(intercom[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-z0-9=_]{60}|[a-h0-9]{8}-[a-h0-9]{4}-[a-h0-9]{4}-[a-h0-9]{4}-[a-h0-9]{12})[\'"]', []))
    tokensList.append(Token('IONIC API KEY', '(ionic[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"](ion_[a-z0-9]{42})[\'"]', []))
    tokensList.append(Token('JENKINS CREDS', '<[a-zA-Z]*>{[a-zA-Z0-9=+/]*}<', []))
    tokensList.append(Token('JSON WEB TOKEN', '(ey[0-9a-z]{30,34}\\.ey[0-9a-z\\/_\\-]{30,}\\.[0-9a-zA-Z\\/_\\-]{10,}={0,2})', []))
    tokensList.append(Token('LINEAR API KEY', '(lin_api_[a-zA-Z0-9]{40})', []))
    tokensList.append(Token('LINEAR CLIENT SECRET/ID', '((linear[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-f0-9]{32})[\'"])', []))
    tokensList.append(Token('LINKEDIN CLIENT ID', 'linkedin(.{0,20})?[\'"][0-9a-z]{12}[\'"]', []))
    tokensList.append(Token('LINKEDIN SECRET KEY', 'linkedin(.{0,20})?[\'"][0-9a-z]{16}[\'"]', []))
    tokensList.append(Token('LOB API KEY', '((lob[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]((live|test)_[a-f0-9]{35})[\'"])|((lob[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]((test|live)_pub_[a-f0-9]{31})[\'"])', []))
    tokensList.append(Token('LOB PUBLISHABLE API KEY', '((test|live)_pub_[a-f0-9]{31})', []))
    tokensList.append(Token('MAILBOXVALIDATOR', '(mailbox.?validator[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([A-Z0-9]{20})[\'"]', []))
    tokensList.append(Token('MAILCHIMP API KEY', '[0-9a-f]{32}-us[0-9]{1,2}', []))
    tokensList.append(Token('MAILGUN API KEY', 'key-[0-9a-zA-Z]{32}\'', []))
    tokensList.append(Token('MAILGUN PUBLIC VALIDATION KEY', 'pubkey-[a-f0-9]{32}', []))
    tokensList.append(Token('MAILGUN WEBHOOK SIGNING KEY', '[a-h0-9]{32}-[a-h0-9]{8}-[a-h0-9]{8}', []))
    tokensList.append(Token('MAPBOX API KEY', '(pk\\.[a-z0-9]{60}\\.[a-z0-9]{22})', []))
    tokensList.append(Token('MESSAGEBIRD API KEY & API CLIENT ID', '(messagebird[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-z0-9]{25}|[a-h0-9]{8}-[a-h0-9]{4}-[a-h0-9]{4}-[a-h0-9]{4}-[a-h0-9]{12})[\'"]', []))
    tokensList.append(Token('MICROSOFT TEAMS WEBHOOK', 'https:\\/\\/[a-z0-9]+\\.webhook\\.office\\.com\\/webhookb2\\/[a-z0-9]{8}-([a-z0-9]{4}-){3}[a-z0-9]{12}@[a-z0-9]{8}-([a-z0-9]{4}-){3}[a-z0-9]{12}\\/IncomingWebhook\\/[a-z0-9]{32}\\/[a-z0-9]{8}-([a-z0-9]{4}-){3}[a-z0-9]{12}', []))
    tokensList.append(Token('NEW RELIC USER API KEY, USER API ID & INGEST BROWSER API KEY', '(NRAK-[A-Z0-9]{27})|((newrelic[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([A-Z0-9]{64})[\'"])|(NRJS-[a-f0-9]{19})', []))
    tokensList.append(Token('NOWNODES', '(nownodes[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([A-Za-z0-9]{32})[\'"]', []))
    tokensList.append(Token('NPM ACCESS TOKEN', '(npm_[a-zA-Z0-9]{36})', []))
    tokensList.append(Token('ORB INTELLIGENCE ACCESS KEY', '[\'"][a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}[\'"]', []))
    tokensList.append(Token('PASTEBIN API KEY', '(pastebin[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-z0-9]{32})[\'"]', []))
    tokensList.append(Token('PAYPAL BRAINTREE ACCESS TOKEN', 'access_token\\$production\\$[0-9a-z]{16}\\$[0-9a-f]{32}', []))
    tokensList.append(Token('PICATIC API KEY', 'sk_live_[0-9a-z]{32}', []))
    tokensList.append(Token('PINATA API KEY', '(pinata[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-z0-9]{64})[\'"]', []))
    tokensList.append(Token('PLANETSCALE API KEY', 'pscale_tkn_[a-zA-Z0-9_\\.\\-]{43}', []))
    tokensList.append(Token('PLANETSCALE OAUTH TOKEN', '(pscale_oauth_[a-zA-Z0-9_\\.\\-]{32,64})', []))
    tokensList.append(Token('PLANETSCALE PASSWORD', 'pscale_pw_[a-zA-Z0-9_\\.\\-]{43}', []))
    tokensList.append(Token('PLAID API TOKEN', '(access-(?:sandbox|development|production)-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', []))
    tokensList.append(Token('PREFECT API TOKEN', '(pnu_[a-z0-9]{36})', []))
    tokensList.append(Token('POSTMAN API KEY', 'PMAK-[a-fA-F0-9]{24}-[a-fA-F0-9]{34}', []))
    tokensList.append(Token('PRIVATE KEYS', '\\-\\-\\-\\-\\-BEGIN PRIVATE KEY\\-\\-\\-\\-\\-|\\-\\-\\-\\-\\-BEGIN RSA PRIVATE KEY\\-\\-\\-\\-\\-|\\-\\-\\-\\-\\-BEGIN OPENSSH PRIVATE KEY\\-\\-\\-\\-\\-|\\-\\-\\-\\-\\-BEGIN PGP PRIVATE KEY BLOCK\\-\\-\\-\\-\\-|\\-\\-\\-\\-\\-BEGIN DSA PRIVATE KEY\\-\\-\\-\\-\\-|\\-\\-\\-\\-\\-BEGIN EC PRIVATE KEY\\-\\-\\-\\-\\-', []))
    tokensList.append(Token('PULUMI API KEY', 'pul-[a-f0-9]{40}', []))
    tokensList.append(Token('PYPI UPLOAD TOKEN', 'pypi-AgEIcHlwaS5vcmc[A-Za-z0-9_\\-]{50,}', []))
    tokensList.append(Token('QUIP API KEY', '(quip[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-zA-Z0-9]{15}=\\|[0-9]{10}\\|[a-zA-Z0-9\\/+]{43}=)[\'"]', []))
    tokensList.append(Token('RUBYGEM API KEY', 'rubygems_[a-f0-9]{48}', []))
    tokensList.append(Token('README API TOKEN', 'rdme_[a-z0-9]{70}', []))
    tokensList.append(Token('SENDGRID API KEY', 'SG\\.[a-zA-Z0-9_\\.\\-]{66}', []))
    tokensList.append(Token('SENDINBLUE API KEY', 'xkeysib-[a-f0-9]{64}-[a-zA-Z0-9]{16}', []))
    tokensList.append(Token('SHIPPO API KEY, ACCESS TOKEN, CUSTOM ACCESS TOKEN, PRIVATE APP ACCESS TOKEN & SHARED SECRET', 'shippo_(live|test)_[a-f0-9]{40}|shpat_[a-fA-F0-9]{32}|shpca_[a-fA-F0-9]{32}|shppa_[a-fA-F0-9]{32}|shpss_[a-fA-F0-9]{32}', []))
    tokensList.append(Token('SIDEKIQ SECRET', '([a-f0-9]{8}:[a-f0-9]{8})', []))
    tokensList.append(Token('SIDEKIQ SENSITIVE URL', '([a-f0-9]{8}:[a-f0-9]{8})@(?:gems.contribsys.com|enterprise.contribsys.com)', []))
    tokensList.append(Token('SLACK TOKEN', 'xox[baprs]-([0-9a-zA-Z]{10,48})?', []))
    tokensList.append(Token('SLACK WEBHOOK', 'https://hooks.slack.com/services/T[a-zA-Z0-9_]{10}/B[a-zA-Z0-9_]{10}/[a-zA-Z0-9_]{24}', []))
    tokensList.append(Token('SMARKSHEEL API KEY', '(smartsheet[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-z0-9]{26})[\'"]', []))
    tokensList.append(Token('SQUARE ACCESS TOKEN', 'sqOatp-[0-9A-Za-z_\\-]{22}', []))
    tokensList.append(Token('SQUARE API KEY', 'EAAAE[a-zA-Z0-9_-]{59}', []))
    tokensList.append(Token('SQUARE OAUTH SECRET', 'sq0csp-[ 0-9A-Za-z_\\-]{43}', []))
    tokensList.append(Token('STYTCH API KEY', 'secret-.*-[a-zA-Z0-9_=\\-]{36}', []))
    tokensList.append(Token('STRIPE ACCESS TOKEN & API KEY', '(sk|pk)_(test|live)_[0-9a-z]{10,32}|k_live_[0-9a-zA-Z]{24}', []))
    tokensList.append(Token('TELEGRAM BOT API TOKEN', '[0-9]+:AA[0-9A-Za-z\\\\-_]{33}', []))
    tokensList.append(Token('TRELLO API KEY', '(trello[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([0-9a-z]{32})[\'"]', []))
    tokensList.append(Token('TWILIO API KEY', 'SK[0-9a-fA-F]{32}', []))
    tokensList.append(Token('TWITCH API KEY', '(twitch[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([a-z0-9]{30})[\'"]', []))
    tokensList.append(Token('TWITTER CLIENT ID', '[tT][wW][iI][tT][tT][eE][rR](.{0,20})?[\'"][0-9a-z]{18,25}', []))
    tokensList.append(Token('TWITTER BEARER TOKEN', '(A{22}[a-zA-Z0-9%]{80,100})', []))
    tokensList.append(Token('TWITTER OAUTH', '[tT][wW][iI][tT][tT][eE][rR].{0,30}[\'"\\\\s][0-9a-zA-Z]{35,44}[\'"\\\\s]', []))
    tokensList.append(Token('TWITTER SECRET KEY', '[tT][wW][iI][tT][tT][eE][rR](.{0,20})?[\'"][0-9a-z]{35,44}', []))
    tokensList.append(Token('TYPEFORM API KEY', 'tfp_[a-z0-9_\\.=\\-]{59}', []))
    tokensList.append(Token('YANDEX ACCESS TOKEN', '(t1\\.[A-Z0-9a-z_-]+[=]{0,2}\\.[A-Z0-9a-z_-]{86}[=]{0,2})', []))
    tokensList.append(Token('YANDEX API KEY', '(AQVN[A-Za-z0-9_\\-]{35,38})', []))
    tokensList.append(Token('YANDEX AWS ACCESS TOKEN', '(YC[a-zA-Z0-9_\\-]{38})', []))
    tokensList.append(Token('WEB3 API KEY', '(web3[a-z0-9_ \\.,\\-]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}[\'"]([A-Za-z0-9_=\\-]+\\.[A-Za-z0-9_=\\-]+\\.?[A-Za-z0-9_.+/=\\-]*)[\'"]', []))
    tokensList.append(Token('GENERIC SECRET', '[sS][eE][cC][rR][eE][tT].*[\'"][0-9a-zA-Z]{32,45}[\'"]', []))
    tokensList.append(Token('BASIC AUTH', '//(.+):(.+)@', []))
    tokensList.append(Token('PHP PASSWORDS', '(pwd|passwd|password|PASSWD|PASSWORD|dbuser|dbpass|pass\').*[=:].+|define ?\\(\'(\\w*pass|\\w*pwd|\\w*user|\\w*datab)', []))
    tokensList.append(Token('SIMPLE PASSWORDS', 'passw.*[=:].+', []))
    tokensList.append(Token('USERNAMES', 'username.*[=:].+', []))
    tokensList.append(Token('NET USER ADD', 'net user .+ /add', []))

## Tokens which need two keys to be interesting ##

    googleSecret = Token('GOOGLE_SECRET', '(\'|\"|\=)(?=(.*[0-9].*))(?=(.*[A-Z].*))(?=([0-9A-Za-z-_]{24})(\1|\'|\"|(\s*(\r\n|\r|\n))))(?!.*\1.*\1.*)(?=(.*[a-z].*))(.*)(\1|\'|\"|(\s*(\r\n|\r|\n)))', None, 2)
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
