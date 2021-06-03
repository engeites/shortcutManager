# from loader import sg
import PySimpleGUI as sg

from database import save_to_av_prices, load_from_database

GRAPH_WIDTH = 160  # each individual graph size in pixels
GRAPH_HEIGHT = 160
TRANSPARENCY = .8  # how transparent the window looks. 0 = invisible, 1 = normal window
NUM_COLS = 4
POLL_FREQUENCY = 1500  #


def check_input(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def better_layout():
    top_col = sg.Column(
        [
            [sg.Text("TOKEN DETAILS",
                     auto_size_text=True,
                     size=(30, 1),
                     font=("Helvetica", 16),
                     justification='center',
                     key="token",
                     pad=((5, 5), (5, 10)))]
        ],
        justification='center'
    )

    col1 = sg.Column(
        [
            [sg.Text("Amount:", size=(10, 1), background_color="white", text_color='black')],
            [sg.Text("Current price:", background_color="white", text_color='black')],
            [sg.Text("In USDT:", background_color="white", text_color='black')]
        ],
        background_color='white',
        element_justification="left"
    )

    col2 = sg.Column(
        [
            [sg.Text("****", key="amount", size=(12, 1), justification='right', background_color="white",
                     text_color='black')],
            [sg.Text("****", key="curr_price", size=(12, 1), justification='right', background_color="white",
                     text_color='black')],
            [sg.Text("****", key="curr_USDT", size=(12, 1), justification='right', background_color="white",
                     text_color='black')]
        ],
        background_color='white',
        element_justification="right"
    )

    col3 = sg.Column(
        [
            [sg.Text("Average price:", size=(10, 1), background_color="white", key="av_pr", enable_events=True,
                     text_color='black')],
            [sg.Text("USDT spent:", background_color="white", text_color='black')],
            [sg.Text("Difference:", background_color="white", text_color='black')],
            [sg.Text("", background_color="white")]
        ],
        background_color='white',
        element_justification="left"
    )

    col4 = sg.Column(
        [
            [sg.Text("****", key="av_price", size=(12, 1), justification='right', background_color="white",
                     text_color='black'),
             sg.InputText("", visible=False, size=(4, 1), key="set_price"),
             sg.Button("Ok", visible=False, bind_return_key=True, key="set_av_price")],
            [sg.Text("****", key="USDT_spent", size=(12, 1), justification='right', background_color="white",
                     text_color='black')],
            [sg.Text("****", key="difference", size=(12, 1), justification='right', background_color="white",
                     text_color='black')],
            [sg.Text("", background_color="white")]
        ],
        background_color='white',
        element_justification="right"
    )

    bot_col = sg.Column([
        [sg.Text("OUTCOME:", font=("Helvetica", 12), text_color='grey'),
         sg.Text("?", key="graphpic", font=("Helvetica", 16)),
         sg.Text("$***", size=(20, 1), key="result", font=("Helvetica", 12)), sg.Button("Close", key="Exit")]
    ],
        pad=((0, 5), (5, 5)))

    left_col = sg.Column([[sg.Text("", background_color="white")], [col1, col2],
                          [sg.Text("", background_color='white', pad=(0, 0), text_color="black")]],
                         background_color='white')
    right_col = sg.Column([[col3, col4]], background_color='white')

    graph_col = sg.Column(
        [[sg.Graph((GRAPH_WIDTH, GRAPH_HEIGHT), (0, 0), (GRAPH_WIDTH, 100), background_color='white', key='_GRAPH_')]],
        vertical_alignment='top', pad=((5, 5), (5, 5)))

    main_col = sg.Column(
        [
            [sg.Column([[left_col]], background_color='white')],
            [sg.Column([[right_col]], background_color='white')]
        ],
        pad=((5, 5), (5, 5))
    )

    layout = [
        [top_col],
        [main_col, graph_col],
        [bot_col]]
    return layout


def calculate(av_price, window):
    amount = window['amount'].DisplayText
    bought_at = window['curr_USDT'].DisplayText
    summ = round(float(amount) * float(av_price))
    window['USDT_spent'].update(value=summ)
    diff = float(bought_at) - summ
    window['difference'].update(value=f"${diff}")
    if diff > 0:
        window["graphpic"].update(value="📈", text_color='green')
        result_text = f"${diff} earned for now"
        window["result"].update(value=result_text)
    elif diff < 0:
        window["graphpic"].update(value="📉", text_color='red')
        result_text = f"${diff} lost for now"
        window["result"].update(value=result_text)


def on_start(payload, window):

    def calculate_current_usdt(curr_price, amount):
        return round(float(curr_price) * float(amount))

    token = payload['token']
    price = payload['price']
    amount = payload['amount']

    usdt_for_now = calculate_current_usdt(price, amount)

    current_av_price_data = load_from_database(token.upper())
    if not current_av_price_data:
        current_av_price_data = 0
        usdt_spent = 0
        diff = 0
    else:
        usdt_spent = round(current_av_price_data * amount)
        diff = usdt_for_now - usdt_spent

    window["amount"].update(value=amount)
    window["curr_price"].update(value=price)
    window["token"].update(value=f"{token} details".upper())
    window["curr_USDT"].update(value=usdt_for_now)
    window["av_price"].update(value=current_av_price_data)
    window["USDT_spent"].update(value=usdt_spent)
    window["difference"].update(value=diff)
    if diff > 0:
        window["graphpic"].update(value="📈", text_color='green')
        result_text = f"{diff}$ earned for now"
        window["result"].update(value=result_text, text_color='green')
    elif diff < 0:
        window["graphpic"].update(value="📉", text_color='red')
        result_text = f"{diff}$ lost for now"
        window["result"].update(value=result_text, text_color='red')


def draw_window(layout):
    window = sg.Window("Details",
                       layout,
                       element_padding=((5, 5), (0, 0)),
                       no_titlebar=True,
                       keep_on_top=True,
                       border_depth=0,
                       grab_anywhere=True,
                       finalize=True
                       )
    return window


def create_details_window(payload):
    layout = better_layout()
    window = draw_window(layout)
    on_start(payload, window)
    while True:
        event, values = window.read(timeout=50)
        if event == "Exit":
            break
        if event == "av_pr":
            window["av_price"].update(visible=False)
            window["set_price"].update(visible=True)
        if event == "set_av_price":
            price = values["set_price"]
            window["av_price"].update(visible=True, value=price)
            window["set_price"].update(visible=False)
            calculate(price, window)
            token = (window['token'].DisplayText).split()[0]
            save_to_av_prices(token.strip(), float(price))
            # TODO: Сделать обновление и создание новых данных в базе приятным процессом.
            #   Подгружать данные в окно детального просмотра при их наличии. При отсутствии -
            #   технично обходить этот момент
    window.close()


if __name__ == '__main__':
    payload = {
        "token": "Pancakebunny",
        "price": 21.25,
        "amount": 8.08}

    layout = better_layout()
    window = draw_window(layout)
    on_start(payload, window)
    while True:
        event, values = window.read(timeout=50)
        if event == "Exit":
            break
        if event == "av_pr":
            window["av_price"].update(visible=False)
            window["set_price"].update(visible=True)
        if event == "set_av_price":
            price = values["set_price"]
            window["av_price"].update(visible=True, value=price)
            window["set_price"].update(visible=False)
            calculate(price, window)

    window.close()
