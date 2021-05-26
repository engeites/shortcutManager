from database.database import Database
db = Database()


# TODO: Move database work to diff.module maybe?
def save_to_database(token, price):
    db.save_to_database(token, price)


def load_from_database(tokens):
    pass