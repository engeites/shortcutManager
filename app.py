from loader import sg

from loader import TXT_COLOR, BG_COLOR

# GET lIST OF TOKENS AND THEIR AMOUNT (DICT)
from loader import tokens
from settings import my_coin_load

# BASIC DATABASE COMMANDS. !!!NOT USED YET!!!
from database import save_to_database

from tokens import TokenDeleter

# FUNCTIONS TO CREATE ALL WINDOWS
from windows import *
from windows.main_window import redraw_time
from windows.settings_window import commit_settings_change

# FUNCTIONS TO PARSE CURRENT PRICES AND EXCHANGE RATES
from parsers import update_prices, check_if_exists

# SOME AUXILIARY FUNCTIONS
from misc import get_current_time, refresh_tokens

# SELF-EXPLANATORY CONSTANTS
from config import REFRESH_PRICES_TIMEOUT, REFRESH_RATE
from config import MAIN_THEME

# A GLOBAL DICTIONARY TO STORE CURRENT PRICES IN MEMORY
current_prices = {}

# A GLOBAL VARIABLE TO CHECK WHETHER AMOUNTS OR PRICES OF TOKENS ARE CURRENTLY SHOWN ON MAIN WINDOW
# If True = token amounts are shown. If False - prices are shown
amount_shown = False

sg.theme(MAIN_THEME)


# TODO: Add a decent logger finally


def save_all_to_database(payload):
    """Saves current prices for all the tokens in tokens list to the database

    :param payload: dict {"Bitcoin": 37892.1,...}
    """
    for token in tokens:
        save_to_database(token, payload[token])
# TODO: DATABASE LOGGING IS NOT WORKING. CURRENTLY NOTHING SAVED IN DB

def on_start(window):
    """This function launches all the other functions needed to display data needed on the man window"""
    redraw_prices(window)


# TODO: maybe move this func to some module?
def convert_usdrub(window):
    """This function swaps total_sum on main window between usd and rub"""
    total_sum = window["total_sum"].DisplayText
    exchange_rate = float(window["exchange_rate"].DisplayText)

    if total_sum[0] == "$":
        try:
            new_sum = round(float(total_sum[1:]) * exchange_rate)
        except ValueError as e:
            new_sum = "****"
        window["total_sum"].update(f"₽{new_sum}")

    elif total_sum[0] == "₽":
        reload_total_sum(window)


def check_if_time_to_refresh_prices(counter):
    if counter == REFRESH_PRICES_TIMEOUT:
        return True
    return False


def reload_total_sum(window):
    """This function simply multiplies current_price by token amount for all the tokens in tokens list"""
    try:
        total_summ = round(sum([current_prices[token] * float(my_coin_load[token]) for token in tokens]))
    except KeyError as e:
        total_summ = "****"
    window["total_sum"].update(f"${total_summ}")


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


# def new_row_layout():
#     return [[sg.Text("Token name",
#                      font=("Arial", 10),
#                      background_color=BG_COLOR,
#                      text_color=TXT_COLOR,
#                      justification="left"
#                      ),
#              sg.Text("****",
#                      font=("Arial", 10),
#                      justification="right",
#                      background_color=BG_COLOR,
#                      text_color=TXT_COLOR,
#                      size=(8, 1)
#                      )
#              ]]


def swap_prices_and_amounts(window):
    global amount_shown, current_prices
    if not amount_shown:
        for token in tokens:
            window[token].update(value=my_coin_load[token])
            amount_shown = True
    else:
        print(current_prices)
        for token in tokens:
            try:
                window[token].update(current_prices[token])
            except KeyError as e:
                window[token].update("****")
        sg.popup_ok("I didn't find token slug in current_prices dict. Are you in test mode?",
                    non_blocking=True, keep_on_top=True)
        amount_shown = False


def hide_token(window, token_to_delete):
    window[token_to_delete].update(visible=False)
    window[f"{token_to_delete}_slug"].update(visible=False)
    pass


def hide_to_system_tray(window):
    menu_def = ['BLANK', ['&Open', '---', '&Save', ['1', '2', ['a', 'b']], '&Properties', 'E&xit']]
    tray = sg.SystemTray(menu=menu_def,  filename=r'icon.png')
    while True:  # The event loop
        menu_item = tray.read()
        print(menu_item)
        if menu_item == 'Exit':
            break
        elif menu_item == 'Open':
            sg.popup('Menu item chosen', menu_item)
        if menu_item == "__DOUBLE_CLICKED__":
            window.UnHide()
            tray.close()
            break


def check_if_amount_is_correct(amount):
    try:
        r = float(amount)
        return True
    except ValueError:
        return False


def main():
    counter = 0

    window = create_main_window()
    # on_start(window)

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
                token_exists = check_if_exists(result['token'])
                amount_correct = check_if_amount_is_correct(result['amount'])
                if token_exists and amount_correct:
                    if result["token"] in tokens:
                        sg.popup_ok(f"Токен: {result['token']} уже есть в вашем списке. Докупили? Измените количество."
                                    f" Продали? Сначала удалите",
                                    non_blocking=True, keep_on_top=True)
                        continue
                    commit_settings_change(result)
                    tokens.append(result['token'])
                    refresh_tokens(result["token"])
                    refresh_layout(result, window)
                    redraw_prices(window)
                elif not token_exists:
                    sg.popup_ok(f"Токен: {result['token']} не найден на coinmarketcap",
                                non_blocking=True, keep_on_top=True)
                elif not amount_correct:
                    sg.popup_ok(f"Вы ввели неправильное количество. Скорее всего, вообще не число",
                                non_blocking=True, keep_on_top=True)
        if event == "delete_coin":
            token_to_delete = create_delete_token_window()
            if token_to_delete:
                manager = TokenDeleter()
                manager.delete_token(token_to_delete)
                hide_token(window, token_to_delete)

                redraw_prices(window)

        if event == "show_token_amounts":
            swap_prices_and_amounts(window)

        if event == "hide_window":
            window.hide()
            hide_to_system_tray(window)

            # TODO: ДОБАВИТЬ ДОКУМЕНТАЦИЮ В ПАКЕТЫ И МОДУЛИ В НИХ, ОПИСАТЬ КЛАССЫ.

            # TODO: СДЕЛАТЬ ЛОГГИРОВАНИЕ!!!

            # TODO: ПЕРЕИМЕНОВАТЬ НЕКОТОРЫЕ ИЗ ЭЛЕМЕНТОВ ГЛАВНОГО ОКНА, ДАТЬ БОЛЕЕ ГОВОРЯЩИЕ НАЗВАНИЯ
        if event == "status":
            sg.popup_ok(my_coin_load, non_blocking=True, keep_on_top=True)
        if event == "total_sum":
            convert_usdrub(window)


if __name__ == '__main__':
    main()
