from importlib import reload
from settings import my_loads


class TokenAmountEditer:

    def __init__(self, token, new_amount):
        self.token = token
        self.amount = new_amount

    @staticmethod
    def __change_my_loads(token, new_amount):
        my_loads.my_coin_load[token] = new_amount
        return my_loads.my_coin_load

    @staticmethod
    def __rewrite_my_loads(payload):
        with open('settings/my_loads.py', 'w', encoding="utf-8" ) as fout:
            fout.write(f"my_coin_load = {str(payload)}")
        print(True)
        return True

    def edit(self):
        payload = self.__change_my_loads(self.token, self.amount)
        self.__rewrite_my_loads(payload)
        reload(my_loads)
        print("Reloaded")

# TODO: MAKE THIS MODULE WORK
