from loader import sg
from loader import tokens
from parsers import update_prices


def create_layout(r: int):
    layout = [
        [sg.Text("Fetching data for you ", key="info", size=(40, 1))],
        [sg.ProgressBar(r,
                        orientation='h',
                        size=(20, 20),
                        key='progressbar',
                        pad=((0,0), (0,0)),
                        style='alt',
                        bar_color=('green', 'white'))]
    ]
    return layout


def create_loading_window(r):
    layout = create_layout(r)
    window = sg.Window('Custom Progress Meter',
                       layout,
                       element_padding=(0, 0),
                       no_titlebar=True)
    return window


def load_prices_on_startup():
    info_text = "Fetching data for you"
    current_prices = {}
    r = len(tokens)
    loading_window = create_loading_window(r)
    progress_bar = loading_window['progressbar']

    for j, token in enumerate(tokens):
        token_price = update_prices([token]) # {'bitcoin': 125512}
        # logger.debug(token_price)
        current_prices[token] = token_price[token]
        event, values = loading_window.read(timeout=10)
        if len(loading_window['info'].DisplayText) > 39:
            loading_window['info'].update(value=info_text)
        else:
            loading_window['info'].update(value=loading_window['info'].DisplayText + "|")
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            pass
        progress_bar.UpdateBar(j+1)

    loading_window.close()
    return current_prices
