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
from collections import Counter, defaultdict

import utils


class Tables(enum.Enum):
    ADS = "ads"
    NEW_ADS = "new_ads"
    SUMMARY = "summary"


EXAMPLE_IMG = "https://www.treidplas.bg/wp-content/uploads/2014/06/default-placeholder.png"
DATABASE = os.path.join(os.getcwd(), "data",  "listings_data.db")


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
    all_locations = [loc.value for loc in list(utils.constants.AdLocation)]
    return random.choice(all_locations)


def get_random_source() -> str:
    """
    It returns a random string from a list of strings
    :return: A random source from the list of all sources.
    """
    all_sources = [source.value for source in list(utils.constants.AdSource)]
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
    return random.choice([home.value for home in list(utils.constants.HomeType)])


def build_data_entry():
    """
    It generates a random entry for a real estate website
    :return: A tuple of 9 elements.
    """

    source_name = get_random_source()
    taken_from = ".".join([source_name, "bg"])
    url = "https://" + "/".join([taken_from, str(random.choice(range(100)))])
    price = get_random_price()
    home_type = get_home_type()
    home_size = get_random_home_size()
    location = get_random_location()
    image = EXAMPLE_IMG
    scraping_date = get_current_date()
    return source_name, url, price, home_type, home_size, location, image, scraping_date, taken_from


def build_dataset(amount) -> list:
    """
    It returns a list of data entries, where each data entry is a dictionary with a random number of
    keys and values

    :param amount: The amount of data entries to generate
    :return: A list of dictionaries.
    """
    return [build_data_entry() for _ in range(amount)]


def build_summary_dataset(dataset) -> Counter:
    """
    It takes a dataset and returns a dictionary of the number of listings per source

    :param dataset: a list of tuples, where each tuple is a listing and its source
    :return: A dictionary with the source as the key and the number of listings as the value.
    """
    all_sources = defaultdict(int)
    # Initial population of the dictionary
    for source in list(utils.constants.AdSource):
        all_sources[source.value]
    # collect the sources that have listings
    sources = [x[0] for x in dataset]
    source_counter = Counter(sources)
    all_sources.update(source_counter)
    return all_sources


def create_ads_table(conn, table_name):
    """
    Inital creation of the ads tables.
    """
    sql = f'''
    CREATE TABLE {table_name} (
    id INTEGER PRIMARY KEY,
	source_name TEXT NOT NULL,
	url TEXT NOT NULL,
	price INTEGER NOT NULL,
	home_type TEXT NOT NULL,
	home_size INTEGER NOT NULL,
    location TEXT NOT NULL,
    image TEXT NOT NULL,
    scraping_date TEXT NOT NULL,
    taken_from TEXT NOT NULL
);
    '''
    cur = conn.cursor()
    cur.execute(sql)


def create_summary_table(conn):
    """
    Initial creation of the summary table.
    """
    sql = f'''
    CREATE TABLE {Tables.SUMMARY.value} (
    id INTEGER PRIMARY KEY,
    addressbg INTEGER NOT NULL,
    arcoreal INTEGER NOT NULL,
    avista INTEGER NOT NULL,
    bulgarianproperties INTEGER NOT NULL,
    era INTEGER NOT NULL,
    galardo INTEGER NOT NULL,
    home2u INTEGER NOT NULL,
    imotbg INTEGER NOT NULL,
    luximmo INTEGER NOT NULL,
    mirelabg INTEGER NOT NULL,
    novdom1 INTEGER NOT NULL,
    place2live INTEGER NOT NULL,
    primoplus INTEGER NOT NULL,
    superimoti INTEGER NOT NULL,
    ues INTEGER NOT NULL,
    yavlena INTEGER NOT NULL,
    yourhome INTEGER NOT NULL
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
    create_summary_table(conn)


def add_entry(conn, table, entry):
    """
    Add entry into the ads table.
    :param conn:
    :param table:
    :param entry:
    :return: entry id
    """
    sql = f''' INSERT INTO {table}(source_name, url, price, home_type, home_size, location, image, scraping_date, taken_from)
              VALUES(?,?,?,?,?,?,?,?,?);'''
    cur = conn.cursor()
    cur.execute(sql, entry)
    conn.commit()
    return cur.lastrowid


def add_summary_entry(conn, entry):
    """
    Add entry into the ads table.
    :param conn:
    :param entry:
    :return: entry id
    """
    collected_sources = entry.keys()
    all_sources_joined = ", ".join(collected_sources)
    expected = ["?" for _ in collected_sources]
    expected_entries = ",".join(expected)
    sql = f'''INSERT INTO {Tables.SUMMARY.value}({all_sources_joined})
              VALUES({expected_entries});'''
    cur = conn.cursor()
    cur.execute(sql, tuple(entry.values()))
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
    conn = create_connection(DATABASE)
    # Generate the needed data
    ads_data = build_dataset(100)
    new_ads_data = build_dataset(25)
    summary_data = build_summary_dataset(new_ads_data)

    with conn:
        # Generate the tables and add the needed entries
        generate_tables(conn)
        for entry in ads_data:
            add_entry(conn, Tables.ADS.value, entry)
        for new_entry in new_ads_data:
            add_entry(conn, Tables.NEW_ADS.value, new_entry)
        add_summary_entry(conn, summary_data)
        show(conn, Tables.SUMMARY.value)
