from loader import sg

from loader import TXT_COLOR, BG_COLOR

# GET lIST OF TOKENS AND THEIR AMOUNT (DICT)
from loader import tokens
from settings import my_coin_load

# BASIC DATABASE COMMANDS. !!!NOT USED YET!!!
from database import save_to_database

# FUNCTIONS TO CREATE DIFFERENT WINDOWS
from windows import create_main_window, \
    create_add_token_window, \
    create_delete_token_window, \
    create_settings_window, \
    refresh_layout

from windows.main_window import redraw_time, create_layout
from windows.settings_window import commit_settings_change

# FUNCTIONS TO PARSE CURRENT PRICES AND EXCHANGE RATES
from parsers import update_prices

# SOME AUXILIARY FUNCTIONS
from misc import get_current_time, refresh_tokens

# SELF-EXPLANATORY CONSTANTS
from config import REFRESH_PRICES_TIMEOUT, REFRESH_RATE
from config import MAIN_THEME

# A GLOBAL VARIABLE TO STORE CURRENT PRICES IN MEMORY
current_prices = {}

sg.theme(MAIN_THEME)


# TODO: Add a decent logger finally


def save_all_to_database(payload):
    """Saves current prices for all the tokens in tokens list to the database

    :param payload: dict {"Bitcoin": 37892.1,...}
    """
    for token in tokens:
        save_to_database(token, payload[token])


def on_start(window):
    """This function launches all the other functions needed to display data needed on the man window"""
    redraw_prices(window)


# TODO: maybe move this func to some module?
def convert_usdrub(window):
    """This function swaps total_sum on main window between usd and rub"""
    total_sum = window["total_sum"].DisplayText
    exchange_rate = float(window["exchange_rate"].DisplayText)

    if total_sum[0] == "$":
        new_sum = float(total_sum[1:]) * exchange_rate
        window["total_sum"].update(f"₽{round(new_sum)}")

    elif total_sum[0] == "₽":
        reload_total_sum(window)


def check_if_time_to_refresh_prices(counter):
    if counter == REFRESH_PRICES_TIMEOUT:
        return True
    return False


def reload_total_sum(window):
    """This function simply multiplies current_price by token amount for all the tokens in tokens list"""
    total_summ = sum([current_prices[token] * float(my_coin_load[token]) for token in tokens])
    window["total_sum"].update(f"${round(total_summ)}")


def redraw_prices(window):
    """This function updates current price for all the window['token'] Text fields when called
    :returns a dict {'Bitcoin': 40000,...} for saving to database"""
    payload = update_prices()
    print(payload)
    print(tokens)
    for token in tokens:
        window[token].update(payload[token])

    global current_prices
    current_prices = payload
    reload_total_sum(window)
    return payload


def new_row_layout():
    return [[sg.Text("Token name",
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
                     size=(8, 1)
                     )
             ]]


"""def refresh_layout(result, window):
    print(result)
    window.extend_layout(window["RIGHT_COL"], new_row_layout())
    # window["RIGHT_COL"].BackgroundColor = BG_COLOR
"""


def main():
    counter = 0

    window = create_main_window()
    on_start(window)

    while True:
        event, values = window.read(timeout=REFRESH_RATE)
        time = get_current_time()
        counter += 100
        time_to_update_prices = check_if_time_to_refresh_prices(counter)
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
            changes_made = create_settings_window()
            if changes_made:
                redraw_prices(window)
                reload_total_sum(window)
        if event == "add_coin":
            result = create_add_token_window()
            if result:
                commit_settings_change(result)
                tokens.append(result['token'])
                refresh_tokens(result["token"])
                refresh_layout(result, window)
        if event == "delete_coin":
            window.extend_layout(window["RIGHT_COL"],
                                 [[sg.Text("token",
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
                                           size=(8, 1))
                                   ]])
            # TODO: СОХРАНЯТЬ ДАННЫЕ НОВОГО ТОКЕНА И ВНЕДРЯТЬ ИХ. КЛЮЧОМ НОВОГО ЭЛЕМЕНТА ТАКЖЕ ДОЛЖЕН БЫТЬ ТОКЕН
            #       СДЕЛАТЬ УДАЛЕНИЕ И ДОБАВЛЕНИЕ ТОКЕНА, ПОСМОТРЕТЬ, БУДЕТ ЛИ ОБНОВЛЯТЬСЯ ЗНАЧЕНИЕ СО ВРЕМЕНЕМ
            #       ВМЕСТЕ С ОСТАЛЬНЫМИ.

            # TODO: ДОБАВИТЬ ДОКУМЕНТАЦИЮ В ПАКЕТЫ И МОДУЛИ В НИХ, ОПИСАТЬ КЛАССЫ.

            # TODO: СДЕЛАТЬ ЛОГГИРОВАНИЕ!!!

            # TODO: ПЕРЕИМЕНОВАТЬ НЕКОТОРЫЕ ИЗ ЭЛЕМЕНТОВ ГЛАВНОГО ОКНА, ДАТЬ БОЛЕЕ ГОВОРЯЩИЕ НАЗВАНИЯ
        if event == "status":
            sg.popup_ok(my_coin_load, non_blocking=True, keep_on_top=True)
        if event == "total_sum":
            convert_usdrub(window)


if __name__ == '__main__':
    main()
