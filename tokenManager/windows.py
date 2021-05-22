from app import sg
from app import tokens
from app import commit_settings_change


def draw_add_token_window():
    col = sg.Column([
        [sg.Text("Добавить токен", size=(50, 1), background_color="light green", pad=((0,0), (0,10)))],
        [sg.Text("Введите тикет токена и купленный объём",
                 font=("Helvetica", 14))],
        [sg.InputText("Токен",
                      key="token",
                      size=(10, 1),
                      font=("Helvetica", 14)
                      ),
         sg.InputText("Количество",
                      key="quantity",
                      size=(10, 1),
                      font=("Helvetica", 14)),
         sg.Ok("Ok")
        ],
    ],
    element_justification="center",
    pad=((5,5), (0,0)))

    layout = [[col]]

    window = sg.Window("Add token",
                       layout,
                       element_padding=((5,5), (0,0)),
                       no_titlebar=True,
                       keep_on_top=True,
                       border_depth=0,
                       grab_anywhere=True
                       )
    event, values = window.read()
    print(event, values)
    window.close()
    return values


def draw_settings_window():
    layout = [[sg.Text("Выберите токен:")],
              [sg.Combo(tokens)],
              [sg.Text("Введите новое количество:")],
              [sg.InputText('100')],
              [sg.Button("Ok"), sg.Cancel("Отмена")]]
    window = sg.Window('Settings',
                       layout,
                       no_titlebar=True,
                       keep_on_top=True,
                       border_depth=0)
    event, values = window.read()
    print(event, values)
    commit_settings_change(values)
    window.close()


def draw_delete_token_window():
    col = sg.Column([
        [sg.Text("Введите тикет токена и купленный объём",
                 font=("Helvetica", 14))],
        [[sg.Combo(tokens)],
         [sg.Ok("Ok")]
         ],
    ],
        element_justification="center")

    layout = [[col]]


if __name__ == '__main__':
    draw_add_token_window()