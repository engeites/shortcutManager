from .coinmarketcap import Parser
from .USDRUB import USDRUBParser

from loader import tokens
coin = Parser()
usd_rub = USDRUBParser()


# GET ALL PRICES FROM COINMARKETCAP
def get_price(token_slug):
    price = coin.get_price(token_slug)
    return price


def update_prices():
    payload = {}
    for token in tokens:
        payload[token] = get_price(token)
    return payload


def get_usd_rub():
    return usd_rub.get_price()