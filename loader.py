# Import base library GUI
import PySimpleGUI as sg

from misc import TokenLoader

# GET TOKEN LIST
token_loader = TokenLoader()
tokens = token_loader.get_tokens()

# LOAD COLOR THEME
BG_COLOR = sg.theme_text_color()
TXT_COLOR = sg.theme_background_color()