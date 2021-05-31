from loader import sg


def check_input(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def calculate_expenses(av_price, amount):
    print(f'multiplying: {av_price} to {amount}')
    return float(av_price) * float(amount)


def calculate_current_usdt(curr_price, amount):
    return float(curr_price) * float(amount)


def create_layout(payload):
    layout = [
        [sg.Text(f"{payload['token'].upper()} TOKEN DETAILS",
                 justification='center',
                 font=('Helvetica', 16))],
        [sg.Text('Amount:'), sg.Text(payload["amount"], key='amount')],
        [sg.Text('Buying price:'), sg.Text("Not Set", size=(10, 1), key='av_price'),
         sg.Button("Set", key="set_buy_price"),
         sg.InputText("hell", size=(8, 1), key="new_price", visible=False),
         sg.Button("Save", key="submit_price", visible=False)],
        [sg.Text("USDT spent in total:"), sg.Text("***", size=(10, 1), key='total_usdt')],
        [sg.Text('Current price:'), sg.Text(payload['price'], size=(10, 1), key='curr_price')],
        [sg.Text('Current USDT:'), sg.Text("***", size=(10, 1), key="current_usdt")],
        [sg.Text('Difference:'), sg.Text('****', key='difference')],
        [sg.Text('Outcome:'), sg.Text("N/A", key="outcome")],
        [sg.Button('Cancel', key="Cancel")]
    ]
    return layout


def draw_window(layout):
    window = sg.Window("Details",
                       layout,
                       element_padding=((5, 5), (0, 0)),
                       no_titlebar=True,
                       keep_on_top=True,
                       border_depth=0,
                       grab_anywhere=True
                       )
    return window


def create_details_window(payload):
    layout = create_layout(payload)
    window = draw_window(layout)

    while True:
        event, values = window.read()
        if event == "set_buy_price":
            window['new_price'].update(visible=True)
            window['submit_price'].update(visible=True)

        if event == 'submit_price':
            if values['new_price']:
                av_price = values['new_price']
                price_format_correct = check_input(av_price)
                if price_format_correct:
                    window['av_price'].update(value=av_price)
                    usdt_spent = calculate_expenses(av_price, window['amount'].DisplayText)
                    current_sum = calculate_current_usdt(window['curr_price'].DisplayText, window['amount'].DisplayText)
                    window['current_usdt'].update(value=current_sum)
                    window['total_usdt'].update(value=usdt_spent)
                    diff = current_sum - usdt_spent
                    window['difference'].update(value=diff)
                    if diff > 0:
                        window['outcome'].update(value='📈')
                    else:
                        window['outcome'].update(value='📉')
            window['new_price'].update(visible=False)
            window['submit_price'].update(visible=False)

        if event == "Cancel":
            window.close()
            return False
