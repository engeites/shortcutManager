from loader import sg, tokens
from tokens import TokenAmountEditer
from settings import my_coin_load


def commit_settings_change(payload):
    token = payload["token"]
    amount = payload["amount"]
    editer = TokenAmountEditer(token, amount)
    editer.edit()
    my_coin_load[token] = amount


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
        commit_settings_change(values)
        window.close()
        return True
    elif event == "Cancel":
        window.close()
        return False