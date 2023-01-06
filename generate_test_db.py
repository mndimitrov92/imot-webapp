"""
Utility script to quickly populate the table with data.

Needs to be executed only once.
"""
import sqlite3
import os
from sqlite3 import Error


DATABASE = os.path.join(os.getcwd(), "data",  "my_filtered_ads.db")


def create_connection(db_file):
    """
    Create a database connection to the SQLite database
    specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def create_table(conn):
    sql = '''
    CREATE TABLE ads (
    id INTEGER PRIMARY KEY,
    title TEXT NULL,
	source_name TEXT NOT NULL,
	url TEXT NOT NULL,
	price INTEGER NOT NULL,
	home_type TEXT NOT NULL,
	home_size TEXT NOT NULL,
    location TEXT NOT NULL,
    image TEXT NOT NULL,
    scraping_date TEXT NOT NULL,
    taken_from TEXT NOT NULL
);
    '''
    cur = conn.cursor()
    cur.execute(sql)


def add_entry(conn, entry):
    """
    Add entry into the ads table.
    :param conn:
    :param entry:
    :return: entry id
    """
    sql = ''' INSERT INTO ads(title, source_name, url, price, home_type, home_size, location, image, scraping_date, taken_from)
              VALUES(?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, entry)
    conn.commit()
    return cur.lastrowid


def show(conn):
    """
    Visualize all entries in the ads table.
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM ads")
    rows = cur.fetchall()
    for row in rows:
        print(row)


if __name__ == "__main__":
    conn = create_connection(DATABASE)
    ENTRIES = [
        # Imot bg
        ("My title 1", "imotbg", "https://imot.bg/1", 50000, "Dvistaen", 56, "Suhata reka",
         "https://www.treidplas.bg/wp-content/uploads/2014/06/default-placeholder.png", "27-04-2022", "imot.bg"),
        ("My title 2", "imotbg", "https://imot.bg/2", 500000, "Dvistaen", 87, "Duvenica",
         "https://www.treidplas.bg/wp-content/uploads/2014/06/default-placeholder.png", "27-04-2022", "imot.bg"),
        ("My title 3", "imotbg", "https://imot.bg/3", 100000, "Tristaen", 67, "Durvenica",
         "https://www.treidplas.bg/wp-content/uploads/2014/06/default-placeholder.png", "27-04-2022", "imot.bg"),
        ("My title 4", "imotbg", "https://imot.bg/4", 87000, "Dvistaen", 77, "Suhata reka",
         "https://www.treidplas.bg/wp-content/uploads/2014/06/default-placeholder.png", "27-04-2022", "imot.bg"),
        ("My title 5", "imotbg", "https://imot.bg/5", 99000, "Dvistaen", 90, "Suhata reka",
         "https://www.treidplas.bg/wp-content/uploads/2014/06/default-placeholder.png", "27-04-2022", "imot.bg"),
        # Yavlena
        ("My title 6", "yavlena", "https://yavlena.bg/1", 56000, "Dvistaen", 56, "Suhata reka",
         "https://www.treidplas.bg/wp-content/uploads/2014/06/default-placeholder.png", "27-04-2022", "yavlena.bg"),
        ("My title 7", "yavlena", "https://yavlena.bg/2", 120000, "Tristaen", 87, "Suhata reka",
         "https://www.treidplas.bg/wp-content/uploads/2014/06/default-placeholder.png", "27-04-2022", "yavlena.bg"),
        ("My title 8", "yavlena", "https://yavlena.bg/3", 99999, "Tristaen", 67, "Suhata reka",
         "https://www.treidplas.bg/wp-content/uploads/2014/06/default-placeholder.png", "27-04-2022", "yavlena.bg"),
        ("My title 9", "yavlena", "https://yavlena.bg/4", 77000, "Dvistaen", 77, "Suhata reka",
         "https://www.treidplas.bg/wp-content/uploads/2014/06/default-placeholder.png", "27-04-2022", "yavlena.bg"),
        ("My title 10", "yavlena", "https://yavlena.bg/5", 98000, "Dvistaen", 90, "Durvenica",
         "https://www.treidplas.bg/wp-content/uploads/2014/06/default-placeholder.png", "27-04-2022", "yavlena.bg"),
        # Bulgarian properties
        ("My title 11", "buildagianproperties", "https://buildagianproperties.bg/1", 86000, "Dvistaen", 56, "Suhata reka",
         "https://www.treidplas.bg/wp-content/uploads/2014/06/default-placeholder.png", "27-04-2022", "buildagianproperties.bg"),
        ("My title 12", "buildagianproperties", "https://buildagianproperties.bg/2", 102000, "Tristaen", 87, "Mladost 2",
         "https://www.treidplas.bg/wp-content/uploads/2014/06/default-placeholder.png", "27-04-2022", "buildagianproperties.bg"),
        ("My title 13", "buildagianproperties", "https://buildagianproperties.bg/3", 88000, "Tristaen", 67, "Suhata reka",
         "https://www.treidplas.bg/wp-content/uploads/2014/06/default-placeholder.png", "27-04-2022", "buildagianproperties.bg"),
        ("My title 14", "buildagianproperties", "https://buildagianproperties.bg/4", 69555, "Dvistaen", 77, "Suhata reka",
         "https://www.treidplas.bg/wp-content/uploads/2014/06/default-placeholder.png", "27-04-2022", "buildagianproperties.bg"),
        ("My title 15", "buildagianproperties", "https://buildagianproperties.bg/5", 88888, "Dvistaen", 90, "Durvenica",
         "https://www.treidplas.bg/wp-content/uploads/2014/06/default-placeholder.png", "27-04-2022", "buildagianproperties.bg"),
        # Era
        ("My title 16", "era", "https://era.bg/1", 56000, "Dvistaen", 56, "Suhata reka",
         "https://www.treidplas.bg/wp-content/uploads/2014/06/default-placeholder.png", "27-04-2022", "era.bg"),
        ("My title 17", "era", "https://era.bg/2", 120000, "Tristaen", 150, "Suhata reka",
         "https://www.treidplas.bg/wp-content/uploads/2014/06/default-placeholder.png", "27-04-2022", "era.bg"),
        ("My title 18", "era", "https://era.bg/3", 99999, "Tristaen", 67, "Suhata reka",
         "https://www.treidplas.bg/wp-content/uploads/2014/06/default-placeholder.png", "27-04-2022", "era.bg"),
        ("My title 19", "era", "https://era.bg/4", 77000, "Dvistaen", 100, "Suhata reka",
         "https://www.treidplas.bg/wp-content/uploads/2014/06/default-placeholder.png", "27-04-2022", "era.bg"),
        ("My title 20", "era", "https://era.bg/5", 98000, "Dvistaen", 90, "Durvenica",
         "https://www.treidplas.bg/wp-content/uploads/2014/06/default-placeholder.png", "27-04-2022", "era.bg"),
    ]

    with conn:
        # Add entries
        create_table(conn)
        for entry in ENTRIES:
            add_entry(conn, entry)
        show(conn)
