from database.database import Database
from .database import AveragePrices
db = Database()

database = AveragePrices()

def save_to_database(token, price):
    pass


def load_from_database(token):
    data = database.get_one(token)
    if data is None:
        return False
    return data[0]


def save_to_av_prices(token, price):
    r = database.check_if_token_in_base(token.strip())
    if not r:
        r = database.add_entry(token, price)
        print("saved to database. New entry")
        return True
    else:
        r = database.update_price(token, price)
        print("saved to database. Updated data")
