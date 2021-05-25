from loader import sg


def create_add_token_window():
    col = sg.Column([
        [sg.Text("Добавить токен", size=(50, 1), background_color="light green", pad=((0, 0), (0, 10)))],
        [sg.Text("Введите тикет токена и купленный объём",
                 font=("Helvetica", 14))],
        [sg.InputText("Токен",
                      key="token",
                      size=(10, 1),
                      font=("Helvetica", 14)
                      ),
         sg.InputText("Количество",
                      key="amount",
                      size=(10, 1),
                      font=("Helvetica", 14)),
         sg.Ok("Ok"),
         sg.Cancel("Cancel")
         ],
    ],
        element_justification="center",
        pad=((5, 5), (0, 0)))

    layout = [[col]]

    window = sg.Window("Add token",
                       layout,
                       element_padding=((5, 5), (0, 0)),
                       no_titlebar=True,
                       keep_on_top=True,
                       border_depth=0,
                       grab_anywhere=True
                       )
    event, values = window.read()
    print(event, values)
    window.close()
    if event == "Cancel":
        return False
    return values
