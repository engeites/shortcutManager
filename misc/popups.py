from loader import sg
from importlib import reload
import lang_congfig
COMMANDS_EN = {
    "token_already_in_wallet": "Token you tried to add is already in your wallet. Please open 'edit'"
                               "window and edit amount if you bought some more",
    "token_not_exists": "Token you typed in was not found on coinmarketcap",
    "amount_not_correct": "The amount you typed in has wrong format. Please make sure it's a number"
}

COMMANDS_RU = {
    "token_already_in_wallet": "Токен что вы добавили уже есть в вашем кошельке",
    "token_not_exists": "Токен не был найден на  coinmarketcap",
    "amount_not_correct": "Поле количество было заполнено неправильно. Убедитесь, что внесли целое или дробное число"
}


def set_lang_settings():
    reload(lang_congfig)
    from lang_congfig import INTERFACE_LANGUAGE
    return INTERFACE_LANGUAGE


def check_lang_settings(INTERFACE_LANGUAGE):
    if INTERFACE_LANGUAGE == 'RU':
        COMMANDS = COMMANDS_RU
    else:
        COMMANDS = COMMANDS_EN
    return COMMANDS


def show_popup(command, **qwargs):
    r = set_lang_settings()
    COMMANDS = check_lang_settings(r)
    sg.popup_ok(COMMANDS[command],
                non_blocking=True, keep_on_top=True)
