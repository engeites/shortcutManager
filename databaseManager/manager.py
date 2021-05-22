from databaseManager.database import Database
db = Database()

# TODO: Move database work to diff.module maybe?
def save_to_database(token, price):
    db.manage_tables(token, price)
