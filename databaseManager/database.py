import sqlite3
from sqlite3 import OperationalError
import time

def get_time():
    return time.strftime("%m-%d-%Y|%T")


class Database:
    token = ""


    def __init__(self):
        self.conn = sqlite3.connect('db.sqlite')
        self.cur = self.conn.cursor()

    def close(self):
        self.conn.close()

    def check_if_table_exists(self, token):
        COMMAND = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{token}';"
        r = self.cur.execute(COMMAND).fetchall()
        if len(r) < 1:
            return False
        return True

    def create_table(self, token):
        COMMAND = f"CREATE TABLE IF NOT EXISTS {token}(timedate, price real);"
        self.cur.execute(COMMAND)
        print(f"table {token} created")

    def add_data(self, token, *payload):
        command = f"INSERT INTO {token} VALUES (?, ?)"
        self.cur.execute(command, payload)
        print("success")

    def check_tables(self):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(self.cur.fetchall())

    def delete_table(self, token):
        r = self.cur.execute(f"DROP TABLE {token};")
        print("Table dropped")
        print(r)

    def commit_changes(self):
        self.conn.commit()

    def select_from(self, token):
        r = self.cur.execute(f"SELECT * FROM {token};").fetchall()
        print(r)

    def manage_tables(self, token, price):
        exists = self.check_if_table_exists(token)
        timedate = get_time()
        token = self.translate_to_sql(token)
        if exists:
            self.add_data(token, price, timedate)
            self.commit_changes()
        else:
            self.create_table(token)
            self.add_data(token, price, timedate)
            self.commit_changes()

    def translate_to_sql(self, token):
        new_token = token
        if "-" in token:
            new_token = token.replace("-", "__")
        if "1" in token:
            new_token = token.replace("1", "one_")
        return new_token

    def translate_from_sql(self, token):
        translated = self.translate_to_sql(token)
        self.select_from(token)


if __name__ == '__main__':
    db = Database()
    db.check_tables()
    # TODO: Handle translations to sql lang and reverse