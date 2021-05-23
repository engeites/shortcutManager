import datetime

import PySimpleGUI as sg

# List of user's tokens
from loader import tokens
from settings import my_coin_load

# Basic database commands
from databaseManager import save_to_database

# Parsers to get current prices
from parsers import update_prices, get_usd_rub

from misc import get_current_time, refresh_tokens


# Instruments to add, edit and delete user's tokens
from tokenManager import TokenAmountEditer

# Some constants
from config import REFRESH_PRICES_TIMEOUT
from config import MAIN_THEME


# A variable to store current prices in memory
current_prices = {}

sg.theme(MAIN_THEME)

# TODO: Add a decent logger finally

BG_COLOR = sg.theme_text_color()
TXT_COLOR = sg.theme_background_color()


def save_all_to_database(payload):
    for token in tokens:
        save_to_database(token, payload[token])


def count_summ(prices):
    total_summ = 0
    for token in tokens:
        summ = prices[token] * float(my_coin_load[token])
        total_summ += summ
    return round(total_summ)


def on_start(window):
    # TODO: When it starts, it saves some data to the db. It should not. Fix it
    redraw_prices(window)


def convert_usdrub(window):
    total_sum = window["total_sum"].DisplayText
    exchange_rate = float(window["exchange_rate"].DisplayText)
    print(total_sum, exchange_rate)
    if total_sum[0] == "$":
        new_sum = float(total_sum[1:]) * exchange_rate
        window["total_sum"].update(f"₽{round(new_sum)}")
    elif total_sum[0] == "₽":
        reload_total_sum(window)


def draw_metrics(token):
    return [sg.Text(token,
                    font=("Arial", 10),
                    background_color=BG_COLOR,
                    text_color=TXT_COLOR,
                    justification="left"
                    ),

            sg.Text("****",
                    font=("Arial", 10),
                    justification="right",
                    background_color=BG_COLOR,
                    text_color=TXT_COLOR,
                    size=(8, 1),
                    auto_size_text=True,
                    key=token)]


def check_if_time_for_prices(counter):
    if counter == REFRESH_PRICES_TIMEOUT:
        return True
    return False


def commit_settings_change(payload):
    token = payload["token"]
    amount = payload["amount"]
    editer = TokenAmountEditer(token, amount)
    editer.edit()
    my_coin_load[token] = amount


def draw_settings_window():
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


def draw_window():
    col1 = sg.Column(
        [[sg.Text("DATE", size=(10, 1),
                  key="date",
                  font=('Arial', 12),

                  pad=((0, 0), (0, 0)),
                  justification="left"),
         sg.Text("TIME", size=(10, 1),
                  key="time",
                  font=('Arial', 12),
                  justification="left",
                  pad=((0, 0), (0, 0)),
                  )]
         ],
        element_justification='left', key="COL1", justification="left")

    # TODO: settings button should be replaced. And maybe even work
    col2 = sg.Column([
        [sg.Text("                                      "),
        sg.Text("x",

                enable_events=True,
                key="Exit",
                background_color="red",
                text_color="white",
                pad=((0, 0),(0, 0)),
                justification="right")]],
                element_justification='right',
                justification="right")

    left_col = sg.Column(
        [[
            sg.Text("$****",
                    font=('Haettenschweiler', 40),
                    justification='center',
                    background_color=BG_COLOR,
                    text_color=TXT_COLOR,
                    key="total_sum",
                    enable_events=True,
                    size = (10, 1),
                    pad=((0, 0), (0, 0)))
        ]],
        pad=((0, 20), (0, 0)))

    metrics = [draw_metrics(token) for token in tokens]
    right_col = sg.Column(metrics, pad=((0, 0), (0, 0)),
                          background_color=BG_COLOR,
                          justification='right',
                          element_justification='right')

    col3 = sg.Column(
        [[
            sg.Text("Курс доллара:", enable_events=True, key="status", pad=(5, 0)),
            sg.Text(str(get_usd_rub()), pad=(5, 0), key="exchange_rate")
        ]],
    element_justification="left")

    col4 = sg.Column(
        [[
            sg.Text("добавить",
                    enable_events=True,
                    key="add_coin",
                    justification="right"),
            sg.Text("удалить",
                    enable_events=True,
                    key="delete_coin",
                    justification="right"),
            sg.Text("редактировать",
                    enable_events=True,
                    key="settings",
                    justification="right")

        ]])
    # TODO: col4 Text content is wrong displayed. Fix

    top_col = sg.Column([[col1, col2]], element_justification="left", justification='left')
    mid_col = sg.Column([[left_col, right_col]], background_color=BG_COLOR)
    bottom_col = sg.Column([[col3, col4]])

    layout = [[top_col],
              [mid_col],
              [bottom_col]]

    window = sg.Window(title="",
                       layout=layout,
                       margins=(0, 0),
                       finalize=True,
                       element_justification='center',
                       right_click_menu=sg.MENU_RIGHT_CLICK_EXIT,
                       keep_on_top=True,
                       no_titlebar=True,
                       grab_anywhere=True,
                       alpha_channel=0.8)

    time = get_current_time()
    redraw_time(window, time)
    return window


def reload_total_sum(window):
    summ = 0
    for token in tokens:
        summ += (current_prices[token] * float(my_coin_load[token]))
    window["total_sum"].update(f"${round(summ)}")


def redraw_prices(window):
    payload = update_prices()
    print(payload)
    for token in tokens:
        window[token].update(payload[token])

    global current_prices
    current_prices = payload
    reload_total_sum(window)
    return payload
        # TODO: move save to database func out of here


def redraw_time(window, time):
    window['date'].update(time["current_date"])
    # window['last_update_time'].update(f'Время последнего обновления: {time["current_time"]}')
    window['time'].update(time["current_time"])


def main():
    counter = 0
    refresh_rate = 500

    window = draw_window()
    on_start(window)

    while True:
        event, values = window.read(timeout=refresh_rate)
        time = get_current_time()
        counter += 100
        time_to_update_prices = check_if_time_for_prices(counter)
        if time_to_update_prices:
            counter = 0
            payload = redraw_prices(window)
            save_all_to_database(payload)
            redraw_time(window, time)
        else:
            redraw_time(window, time)

        if event == "Exit":
            break
        if event == "settings":
            changes_made = draw_settings_window()
            if changes_made:
                # redraw_prices(window)
                reload_total_sum(window)
        if event == "add_coin":
            from tokenManager.windows import draw_add_token_window
            result = draw_add_token_window()
            if result:
                commit_settings_change(result)
                tokens.append(result['token'])
                refresh_tokens(result["token"])
        if event == "status":
            sg.popup_ok(my_coin_load, non_blocking=True, keep_on_top=True)
        if event == "total_sum":
            convert_usdrub(window)


if __name__ == '__main__':
    main()
