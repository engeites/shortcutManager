from loader import sg, tokens
from tokens import TokenManager
from settings import my_coin_load
from misc import show_popup
from loader import user_control


def commit_settings_change(payload: dict):
    """
    This function manages all config files with user data: my_loads.py and my_tokens.txt
    It rewrites these files using new tokens and my_token_load variables
    :param payload: dict {"token": 1245}
    :return:
    """
    token = payload["token"]
    amount = payload["amount"]
    editer = TokenManager(token, amount)
    editer.edit_amount()
    my_coin_load[token] = amount


def check_if_correct(values):
    try:
        r = float(values['amount'])
        return True
    except ValueError:
        show_popup("amount_not_correct")
        return False


def create_settings_window():
    layout = [[sg.Text("Выберите токен:")],
              [sg.Combo(tokens, key="token", readonly=True)],
              [sg.Text("Введите новое количество:")],
              [sg.InputText('100', key="amount")],
              [sg.Button("Ok", key="Ok"), sg.Cancel("Отмена", key="Cancel")]]
    window = sg.Window('Settings',
                       layout,
                       no_titlebar=True,
                       keep_on_top=True,
                       border_depth=0)
    event, values = window.read()
    if event == "Ok":
        amount_correct = check_if_correct(values)
        if amount_correct:
            user_control.info(f"User changed amount of {values['token']} to {values['amount']}")
            commit_settings_change(values)
            window.close()
            return True
        user_control.info(f"User tried to change amount of {values['token']} to {values['amount']}")
        return False
    elif event == "Cancel":
        window.close()
        return False