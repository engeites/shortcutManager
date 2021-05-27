from importlib import reload
from settings import my_loads
from loader import tokens
from settings.my_loads import my_coin_load


class TokenManager:
    """This class is used to redefine my_loads variable containing amount of tokens user has
    and rewrite my_loads.py (this file contains a dict 'my_loads'"""

    def __init__(self, token, new_amount=0):
        self.token = token
        self.amount = new_amount

    @staticmethod
    def __change_my_loads(token, new_amount):
        """Redefines amount of token in my_loads variable"""
        my_loads.my_coin_load[token] = new_amount
        return my_loads.my_coin_load

    @staticmethod
    def __rewrite_my_loads(payload):
        """Rewrites my_loads.py file"""
        with open('settings/my_loads.py', 'w', encoding="utf-8") as fout:
            fout.write(f"my_coin_load = {str(payload)}")
        return True

    def edit_amount(self):
        """Main manager method of this class, runs all functions in correct order"""
        payload = self.__change_my_loads(self.token, self.amount)
        self.__rewrite_my_loads(payload)
        reload(my_loads)
        print("Reloaded")


class TokenDeleter:

    @staticmethod
    def __change_my_loads(token):
        print(my_loads.my_coin_load)
        my_loads.my_coin_load.pop(token)
        print(f"new my_loads: {my_loads.my_coin_load}")
        return True

    @staticmethod
    def __rewrite_my_loads(payload):
        with open('settings/my_loads.py', 'w', encoding="utf-8") as fout:
            fout.write(f"my_coin_load = {str(payload)}")

    @staticmethod
    def __rewrite_my_tokens(token):
        print(f"Старый список: {tokens}")
        for i, coin in enumerate(tokens):
            print(i, coin)
            if coin == token:
                print(f"found token: {coin} in tokens. Index: {i}")
                tokens.pop(i)
        print(f"Новый список токенов: {tokens}")
        with open('settings/my_tokens.txt', 'w', encoding='utf-8') as fout:
            for token in tokens:
                fout.write(token + "\n")

    def delete_token(self, token):
        my_loads_changed = self.__change_my_loads(token)
        print(f"my_loads_changed: {my_loads_changed}")
        self.__rewrite_my_loads(my_loads.my_coin_load)
        self.__rewrite_my_tokens(token)
        return True
        # print("Error while deleting token. Check TokenDeleter class")
