# Import base library GUI
import logging.config

import PySimpleGUI as sg

from misc import TokenLoader
from logger_config import logger_config

# SETUP LOGGER
logging.config.dictConfig(logger_config)
logger = logging.getLogger('app_logger')
price_logger = logging.getLogger('price_logger')

logger.debug("App is running")

# GET TOKEN LIST
token_loader = TokenLoader()
tokens = token_loader.get_tokens()

# LOAD COLOR THEME
BG_COLOR = sg.theme_text_color()
TXT_COLOR = sg.theme_background_color()