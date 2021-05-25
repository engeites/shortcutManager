from loader import sg
from loader import BG_COLOR, TXT_COLOR
from parsers import get_usd_rub
from loader import tokens
from misc import get_current_time


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


def redraw_time(window, time):
    window['date'].update(time["current_date"])
    # window['last_update_time'].update(f'Время последнего обновления: {time["current_time"]}')
    window['time'].update(time["current_time"])


def create_main_window():
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