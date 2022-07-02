import sqlite3
import pandas as pd


def to_sqlite():
# load data
    df = pd.read_csv('chats.csv', encoding = "cp1252")
    df.columns = df.columns.str.strip()
    con = sqlite3.connect("chats_db.db")
    df.to_sql("MyTable", con)
    con.close()
    print("done........")

to_sqlite()