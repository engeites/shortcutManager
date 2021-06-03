import sqlite3
from sqlite3 import OperationalError
import time
from config import DATABASE_FILE

def get_time():
    return time.strftime("%m-%d-%Y|%T")


class Database:
    token = ""

    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_FILE)
        self.cur = self.conn.cursor()

    def close(self):
        self.conn.close()

    def check_if_table_exists(self, token):
        COMMAND = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{token}';"
        r = self.cur.execute(COMMAND).fetchall()
        if len(r) < 1:
            return False
        return True


class AveragePrices:

    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_FILE)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        COMMAND = f"CREATE TABLE IF NOT EXISTS av_price(token text, price real);"
        self.cur.execute(COMMAND)

    def check_if_token_in_base(self, token):
        r = self.cur.execute("SELECT token FROM av_price WHERE token=?", (token,)).fetchone()
        print(f"Is token in base? {r}")
        if r is None:
            return False
        return True

    def update_price(self, *payload):
        with self.conn:
            return self.cur.execute("UPDATE av_price SET price = ? WHERE token=?", payload)

    def add_entry(self, *payload):
        with self.conn:
            return self.cur.execute("INSERT INTO 'av_price' ('token', 'price') VALUES (?,?)", payload)

    def get_one(self, token):
        with self.conn:
            try:
                return self.cur.execute("SELECT price FROM av_price WHERE token=?", (token,)).fetchone()
            except OperationalError as e:
                print(f"sqlite Operational Error line 116: {e}")
                return "***"

    def close_connection(self):
        self.conn.close()


if __name__ == '__main__':
    db = Database()
    db.check_tables()
    # TODO: Handle translations to sql lang and reverse