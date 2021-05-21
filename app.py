import PySimpleGUI as sg
import datetime

from misc import Parser, USDRUBParser, TokenLoader
from settings import my_coin_load
from database import Database

from config import UPDATE_FREQUENCY, TIMER, MAIN_THEME

sg.theme(MAIN_THEME)

# TODO: Add a decent logger finally

BG_COLOR = sg.theme_text_color()
TXT_COLOR = sg.theme_background_color()
REFRESH_PRICES_TIMEOUT = 1000 * 60 * 5

# GET TOKEN LIST
token_loader = TokenLoader()
tokens = token_loader.get_tokens()

# CREATING PARSER OBJ TO PARSE PRICES
coin = Parser()
usd_rub = USDRUBParser()

db = Database()

# TODO: Move database work to diff.module maybe?
def save_to_database(token, price):
    db.manage_tables(token, price)


# GET ALL PRICES FROM COINMARKETCAP
def get_price(token_slug):
    price = coin.get_price(token_slug)
    return price


def update_prices():
    payload = {}
    for token in tokens:
        payload[token] = get_price(token)
    return payload


def get_current_time():
    now = datetime.datetime.now()

    cur_date = now.strftime("%Y-%m-%d")
    cur_time = now.strftime("%H:%M:%S")
    return {"current_time": cur_time,
            "current_date": cur_date}


def count_summ(prices):
    total_summ = 0
    for token in tokens:
        summ = prices[token] * my_coin_load[token]
        total_summ += summ
    return round(total_summ)

def on_start(window):
    # TODO: When it starts, it saves some data to the db. It should not. Fix it
    redraw_prices(window)


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
                    size=(8,1),
                    auto_size_text=True,
                    key=token)]


def check_if_time_for_prices(counter):
    if counter == REFRESH_PRICES_TIMEOUT:
        return True
    return False


def draw_window():
    col1 = sg.Column(
        [[sg.Text("TIME", size=(10, 1),
                  key="time",
                  font=('Arial', 25),
                  justification="center",
                  pad=((35, 0), (5, 0)),
                  auto_size_text=True)],
        [sg.Text("DATE", size=(22, 1),
                  key="date",
                  font=('Arial', 12),
                  auto_size_text=True,
                  pad=((35, 0), (0, 0)),
                  justification="center")]],
        element_justification='center', key="COL1")

    # TODO: settings button should be replaced. And maybe even work
    col2 = sg.Column([[sg.Text("edit",
                               enable_events=True,
                               key="settings",
                               justification="right")]],
                     element_justification='right',
                     justification="right"
                     )

    left_col = sg.Column(
        [[
            sg.Text("$****",
                    font=('Haettenschweiler', 60),
                    justification='center',
                    background_color=BG_COLOR,
                    text_color=TXT_COLOR,
                    key="total_sum",
                    size=(5,1),
                    pad=((0, 0), (0, 0)))]],
        pad=((0, 20), (0, 0)))

    metrics = [draw_metrics(token) for token in tokens]
    right_col = sg.Column(metrics, pad=((0, 0), (0, 0)),
                          background_color=BG_COLOR,
                          justification='right',
                          element_justification='right')

    text = f"Курс доллара: {str(usd_rub.get_price())}"
    col3 = sg.Column(
        [[
            sg.Text(text)
        ]])

    col4 = sg.Column(
        [[
            sg.Text("Время последнего обновления: ***", key="last_update_time")
        ]])
    # TODO: col4 Text content is wrong displayed. Fix

    top_col = sg.Column([[col1, col2]])
    mid_col = sg.Column([[left_col, right_col]], background_color=BG_COLOR)
    bottom_col = sg.Column([[col3, col4]])

    layout = [[top_col],
              [mid_col],
              [bottom_col]]

    window = sg.Window(layout=layout, title='Weather Widget', margins=(0, 0), finalize=True,
                       element_justification='center', right_click_menu=sg.MENU_RIGHT_CLICK_EXIT, keep_on_top=True, no_titlebar=True, grab_anywhere=True,
                       alpha_channel=0.8)

    time = get_current_time()
    redraw_time(window, time)
    return window


def redraw_prices(window):
    payload = update_prices()
    for token in tokens:
        window[token].update(payload[token])
        sum = count_summ(payload)
        window['total_sum'].update(f"${sum}")
        save_to_database(token, payload[token])


def redraw_time(window, time):
    window['date'].update(time["current_date"])
    window['last_update_time'].update(f'Время последнего обновления: {time["current_time"]}')
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
            redraw_prices(window)
            redraw_time(window, time)
        else:
            redraw_time(window, time)

        if event == "Exit":
            break
        if event == "settings":
            print("Settings pressed")


if __name__ == '__main__':
    main()