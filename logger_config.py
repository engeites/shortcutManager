
logger_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'std_format': {
            'format': '{asctime} - {levelname} - {name} - {message}',
            'style': "{"
        },
        'file_format': {
            'format': '{asctime} | {levelname} - {module}::{lineno} - {message}',
            'style': "{"
        },
        'prices_format': {
            'format': "{asctime} | The price of {message}",
            'style': "{"
        },
        'user_info_format': {
            'format': '{asctime} | {module}::{lineno} - {message}',
            'style': '{'
        }
    },
    'handlers': {
        'console_handler': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'std_format'
        },
        'file_handler': {
            'filename': 'logs/MainLog.log',
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'formatter': "file_format"
        },
        'token_handler': {
            'filename': 'logs/PricesLog.log',
            'class': 'logging.FileHandler',
            'level': "INFO",
            'formatter': 'prices_format'
        },
        'user_control_handler': {
            'filename': 'logs/UserActions.log',
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'formatter': 'user_info_format'
        }
    },
    'loggers': {
        'app_logger': {
            'level': 'INFO',
            'handlers': ['console_handler', 'file_handler']
        },
        'price_logger': {
            'level': "INFO",
            'handlers': ['token_handler']
        },
        'user_control': {
            'level': 'INFO',
            'handlers': ['user_control_handler']
        }
    }
    # 'filters': {}
}