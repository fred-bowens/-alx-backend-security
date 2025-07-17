INSTALLED_APPS = [
    ...
    'ratelimit',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'loggers': {
        'ratelimit': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
