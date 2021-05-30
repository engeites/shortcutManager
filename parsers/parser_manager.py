from .coinmarketcap import Parser
from .USDRUB import USDRUBParser

coin = Parser()
usd_rub = USDRUBParser()


# GET ALL PRICES FROM COINMARKETCAP
def get_price(token_slug):
    price = coin.get_price(token_slug)
    return price


def check_if_exists(token):
    token_exists = coin.check_if_exists(token)
    if token_exists: return True
    return False


def update_prices(tokens_to_parse):
    payload = {}
    for token in tokens_to_parse:
        payload[token] = get_price(token)
    return payload


def get_usd_rub():
    price = usd_rub.get_price()
    if not price:
        return "No conn"
    return usd_rub.get_price()
