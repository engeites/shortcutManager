from loader import sg
from loader import tokens

def create_delete_token_window():
    col = sg.Column([
        [sg.Text("Введите тикет токена и купленный объём",
                 font=("Helvetica", 14))],
        [[sg.Combo(tokens)],
         [sg.Ok("Ok")]
         ],
    ],
        element_justification="center")

    layout = [[col]]

