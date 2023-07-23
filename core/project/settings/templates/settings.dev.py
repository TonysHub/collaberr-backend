SECRET_KEY = 'django-insecure-9w#1qc84z6&l!konc6lb!+j4$iwwkk&o(tv0!qq85^j_i72nq4'

DEBUG = True


LOGGING['formatters']['colored'] = {  # type: ignore
    '()': 'colorlog.ColoredFormatter',
    'format': '%(log_color)s%(asctime)s %(levelname)s %(name)s %(bold_white)s%(message)s',
}
LOGGING['loggers']['core']['level'] = 'DEBUG'  # type: ignore
LOGGING['handlers']['console']['level'] = 'DEBUG'  # type: ignore
LOGGING['handlers']['console']['formatter'] = 'colored'  # type: ignore

YOUTUBE_SECRETS_FILE = BASE_DIR / 'youtube_secret.json'
YOUTUBE_CREDENTIALS_FILE = BASE_DIR / 'youtube_credential_secret.csv'
