from loader import sg
from loader import logger, price_logger, user_control


# TODO: 1. ИСПРАВИТЬ НАДПИСИ В ОКНАХ add_token, delete_token.
#   2. Добавить поддержку языка во все окна
#   3. Переместить my_coin_loads и другие глоб. переменные в базу данных, не надо хранить в файлах
#   4. Доработать вид и функционал details_window
#   5. Исправить ситуацию с перетаскиванием окна при попытке выделения текста в inputText
#   6. Начать, наконец, хранить историю цен в базе данных
#   7. Добавляем графики или нет????
#   8. Переименовать некоторые из элементов главного и других окон, дать более говорящие ключи
#   9. Обновить и добавить документацию в модули и функции
#   10. Оптимизировать main loop, постараться создать функции-менеджеры вместо длинных описаний в главном цикле


# GET lIST OF TOKENS AND THEIR AMOUNT (DICT)
from loader import tokens
from settings import my_coin_load

# BASIC DATABASE COMMANDS. !!!NOT USED YET!!!
from database import save_to_database
from misc.popups import set_lang_settings
from tokens import TokenDeleter

# FUNCTIONS TO CREATE ALL WINDOWS
from windows import *
from windows.main_window import redraw_time
from windows.settings_window import commit_settings_change

# FUNCTIONS TO PARSE CURRENT PRICES AND EXCHANGE RATES
from parsers import update_prices, check_if_exists

# SOME AUXILIARY FUNCTIONS
from misc import get_current_time, refresh_tokens
from misc import show_popup

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

def set_interface_lang(current_lang):
    if current_lang == "RU":
        with open('lang_congfig.py', 'w', encoding="utf-8") as fout:
            fout.write("INTERFACE_LANGUAGE = 'EN'")
        set_lang_settings()
        user_control.info("INTERFACE LANG was set to EN")
        return "EN"
    elif current_lang == "EN":
        with open('lang_congfig.py', 'w', encoding="utf-8") as fout:
            fout.write("INTERFACE_LANGUAGE = 'RU'")
        set_lang_settings()
        user_control.info("INTERFACE LANG was set to RU")
        return "RU"


def save_all_to_database(payload):
    """Saves current prices for all the tokens in tokens list to the database

    :param payload: dict {"Bitcoin": 37892.1,...}
    """
    for token in tokens:
        save_to_database(token, payload[token])


# TODO: DATABASE LOGGING IS NOT WORKING. CURRENTLY NOTHING SAVED IN DB

def on_start():
    global current_prices
    """This function launches all the other functions needed to display data needed on the man window"""
    prices = load_prices_on_startup()
    current_prices = prices
    logger.info("APP started")


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


def initial_price_drawing(window):
    for token in tokens:
        window[token].update(current_prices[token])


def redraw_prices(window):
    """This function updates current price for all the window['token'] Text fields when called
    :returns a dict {'Bitcoin': 40000,...} for saving to database"""
    payload = update_prices(tokens)
    for token in tokens:
        window[token].update(payload[token])
        price_logger.info(f"{token} = {payload[token]}")
    logger.debug("Just redrew all prices")
    global current_prices
    user_control.info(f"global var current_prices is set to {current_prices}")
    current_prices = payload
    reload_total_sum(window)
    return payload


def swap_prices_and_amounts(window):
    global amount_shown, current_prices
    if not amount_shown:
        for token in tokens:
            window[token].update(value=my_coin_load[token])
            amount_shown = True
    else:
        for token in tokens:
            try:
                window[token].update(current_prices[token])
            except KeyError as e:
                window[token].update("****")
        sg.popup_ok("I didn't find token slug in current_prices dict. Are you in test mode?",
                    non_blocking=True, keep_on_top=True)
        amount_shown = False


def hide_token(window, token_to_delete):
    """
    Simply hides token from params on main window
    :param window: main window object
    :param token_to_delete: str(token)
    :return:
    """
    window[token_to_delete].update(visible=False)
    window[f"{token_to_delete}_slug"].update(visible=False)


def hide_to_system_tray(window):
    menu_def = ['BLANK', ['&Open', '---', '&Save', ['1', '2', ['a', 'b']], '&Properties', 'E&xit']]
    tray = sg.SystemTray(menu=menu_def, filename=r'icon.png')
    logger.debug("APP is hidden to tray")
    while True:  # The event loop
        menu_item = tray.read()
        if menu_item == 'Exit':
            break
        elif menu_item == 'Open':
            sg.popup('Menu item chosen', menu_item)
        if menu_item == "__DOUBLE_CLICKED__":
            window.UnHide()
            tray.close()
            logger.debug("tray icon closed, main window maximized")
            break


def check_if_amount_is_correct(amount):
    try:
        r = float(amount)
        return True
    except ValueError:
        return False


def main():
    # counter variable to check if it is time to update prices on main screen. Default: 5 min
    counter = 0
    global INTERFACE_LANGUAGE

    # Some work we need to do before main window creation
    on_start()

    window = create_main_window()
    initial_price_drawing(window)
    reload_total_sum(window)

    while True:
        event, values = window.read(timeout=REFRESH_RATE)
        # Get time to update DATE and TIME elements on main window
        time = get_current_time()
        counter += 100
        # counter must reach 1000 * 60 * 5 for time_to_update_prices to become True
        time_to_update_prices = check_if_time_to_refresh_prices(counter)

        if time_to_update_prices:
            counter = 0
            logger.info("TIME TO UPDATE PRICES. Counter set to 0")
            # redraw_prices is a big function, that parses data from coinmarketcap and updates
            # most of data on main window (token prices and total sum)
            # TODO: MAYBE THIS FUNC NEEDS RETHINKING? APP FROZES UNTILL PRICES ARE DROWN
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
            new_token_data = create_add_token_window()
            if new_token_data:
                user_control.info(f"User tries to add next data: {new_token_data}")
                token_exists = check_if_exists(new_token_data['token'])
                amount_correct = check_if_amount_is_correct(new_token_data['amount'])
                if token_exists and amount_correct:
                    # Check if we already have this token in tokens list
                    if new_token_data["token"] in tokens:
                        show_popup("token_already_in_wallet", token=new_token_data['token'])
                        continue
                    user_control.info("Data was checked. Token exists, amount is a float number. Token is not in list yet")
                    commit_settings_change(new_token_data)
                    tokens.append(new_token_data['token'])
                    refresh_tokens(new_token_data["token"])
                    refresh_layout(new_token_data, window)
                    redraw_prices(window)
                elif not token_exists:
                    show_popup("token_not_exists", token={new_token_data['token']})

                elif not amount_correct:
                    show_popup("amount_not_correct")

        if event == "delete_coin":
            token_to_delete = create_delete_token_window()
            user_control.info(f"User tries to delete a token: {token_to_delete}")
            if token_to_delete:
                manager = TokenDeleter()
                manager.delete_token(token_to_delete)
                hide_token(window, token_to_delete)
                user_control.info(f"No problems. Token {token_to_delete} is deleted safely")
                redraw_prices(window)

        if event == "show_token_amounts":
            swap_prices_and_amounts(window)

        if event == "hide_window":
            window.hide()
            hide_to_system_tray(window)

        if event == 'swap_lang':
            current_lang = window['swap_lang'].DisplayText
            if current_lang == "EN":
                r = set_interface_lang(current_lang)
                window['swap_lang'].update(value=r)
            elif current_lang == "RU":
                r= set_interface_lang(current_lang)
                window['swap_lang'].update(value=r)

        if event == "status":
            sg.popup_ok(my_coin_load, non_blocking=True, keep_on_top=True)
        if event == "total_sum":
            convert_usdrub(window)
        if event in tokens:
            payload = {
                "token": event,
                "price": window[event].DisplayText,
                "amount": my_coin_load[event]}

            create_details_window(payload)


if __name__ == '__main__':
    main()
