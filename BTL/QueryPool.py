import pandas
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def get_all_users(conn):
    users = pandas.read_sql_query('''
                                  SELECT * FROM users
                                  ''', conn)
    return users

def get_all_songs(conn):
    songs = pandas.read_sql_query('''
                                  SELECT * FROM songs
                                  ''', conn)
    return songs

def get_all_trackings(conn):
    trackings = pandas.read_sql_query('''
                                  SELECT * FROM trackings
                                  ''', conn)
    return trackings


