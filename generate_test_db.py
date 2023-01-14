"""
Utility script to quickly populate the tables with data.

Needs to be executed only once.
"""
import enum
import os
import random
import sqlite3
from sqlite3 import Error
from datetime import datetime

import utils


class Tables(enum.Enum):
    ADS = "ads"
    NEW_ADS = "new_ads"
    SUMMARY = "summary"


EXAMPLE_IMG = "https://www.treidplas.bg/wp-content/uploads/2014/06/default-placeholder.png"


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


# Data preparation
def get_random_location() -> str:
    all_locations = [loc.value for loc in list(utils.AdLocation)]
    return random.choice(all_locations)


def get_random_source() -> str:
    """
    It returns a random string from a list of strings
    :return: A random source from the list of all sources.
    """
    all_sources = [source.value for source in list(utils.AdSource)]
    return random.choice(all_sources)


def get_random_price() -> int:
    """
    It returns a random integer between 50,000 and 300,000
    :return: A random price between 50,000 and 300,000
    """
    return random.choice(range(50_000, 300_000))


def get_random_home_size() -> int:
    """
    > This function returns a random integer between 50 and 200
    :return: A random integer between 50 and 200
    """
    return random.choice(range(50, 200))


def get_current_date() -> str:
    """
    It returns the current date in the format dd-mm-yy
    :return: A string
    """
    return datetime.strftime(datetime.now(), '%d-%m-%y')


def get_home_type():
    """
    It returns a random value from the list of values in the HomeType enum
    :return: A random value from the list of values in the HomeType enum.
    """
    return random.choice([home.value for home in list(utils.HomeType)])


def build_data_entry():
    """
    It generates a random entry for a real estate website
    :return: A tuple of 9 elements.
    """

    source_name = get_random_source()
    url = "https://" + \
        "/".join([".".join([source_name, "bg"]),
                 str(random.choice(range(100)))])
    price = get_random_price()
    home_type = get_home_type()
    home_size = get_random_home_size()
    location = get_random_location()
    image = EXAMPLE_IMG
    scraping_date = get_current_date()
    return source_name, url, price, home_type, home_size, location, image, scraping_date


def build_dataset(amount) -> list:
    """
    It returns a list of data entries, where each data entry is a dictionary with a random number of
    keys and values

    :param amount: The amount of data entries to generate
    :return: A list of dictionaries.
    """
    return [build_data_entry() for _ in range(amount)]


def create_ads_table(conn, table_name):
    """
    Inital creation of the ads tables.
    """
    sql = f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
    id INTEGER PRIMARY KEY,
	source_name TEXT NOT NULL,
	url TEXT NOT NULL,
	price INTEGER NOT NULL,
	home_type TEXT NOT NULL,
	home_size INTEGER NOT NULL,
    location TEXT NOT NULL,
    image TEXT NOT NULL,
    scraping_date TEXT NOT NULL
);
    '''
    cur = conn.cursor()
    cur.execute(sql)


def generate_tables(conn):
    """
    Creates all needed tables - both ads tables and the summary table
    """
    create_ads_table(conn, Tables.ADS.value)
    create_ads_table(conn, Tables.NEW_ADS.value)


def add_entry(conn, table, entry):
    """
    Add entry into the ads table.
    :param conn:
    :param table:
    :param entry:
    :return: entry id
    """
    sql = f''' INSERT INTO {table}(source_name, url, price, home_type, home_size, location, image, scraping_date)
              VALUES(?,?,?,?,?,?,?,?);'''
    cur = conn.cursor()
    cur.execute(sql, entry)
    conn.commit()
    return cur.lastrowid


def show(conn, table):
    """
    Visualize all entries in the ads table.
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table};")
    rows = cur.fetchall()
    for row in rows:
        print(row)


if __name__ == "__main__":
    utils.create_db_folder()
    conn = create_connection(utils.DATABASE)
    # Generate the needed data
    ads_data = build_dataset(100)
    new_ads_data = build_dataset(25)

    with conn:
        # Generate the tables and add the needed entries
        generate_tables(conn)
        for entry in ads_data:
            add_entry(conn, Tables.ADS.value, entry)
        for new_entry in new_ads_data:
            add_entry(conn, Tables.NEW_ADS.value, new_entry)
        show(conn, Tables.NEW_ADS.value)
