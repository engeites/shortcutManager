from loader import sg
from loader import tokens


def create_layout():
    col = sg.Column([
        [sg.Text("Введите тикет токена и купленный объём",
                 font=("Helvetica", 14))],
        [sg.Combo(tokens, key="token"), sg.Ok("Ok"), sg.Cancel("Cancel")],
    ],
        element_justification="center")

    layout = [[col]]
    return layout


def draw_window(layout):
    window = sg.Window("Add token",
                       layout,
                       element_padding=((5, 5), (0, 0)),
                       no_titlebar=True,
                       keep_on_top=True,
                       border_depth=0,
                       grab_anywhere=True
                       )
    return window


def create_delete_token_window():
    layout = create_layout()
    window = draw_window(layout)
    event, values = window.read()
    window.close()
    print(values)
    return values['token']