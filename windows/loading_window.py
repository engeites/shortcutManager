from loader import sg


def create_layout(r:int):
    layout = [
        [sg.ProgressBar(r, orientation='h', size=(20, 20), key='progressbar')],
        [sg.Button("Hello", key="main_button")]
    ]
    return layout


def create_loading_window(r):
    layout = create_layout(r)
    window = sg.Window('Custom Progress Meter', layout)
    return window
