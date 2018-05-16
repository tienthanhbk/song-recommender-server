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

def get_random_songs(conn):
    users = pandas.read_sql_query('''
                                  SELECT * FROM songs
                                  ''', conn)
    users_random = users.sample(n=10)
    return users_random

def search_songs(conn, txtsearch):
    txtsearch_fix = '%'+txtsearch+'%'
    songs = pandas.read_sql_query('''
        SELECT * FROM songs WHERE LOWER(song_name) LIKE ?
            OR LOWER(artist_name) LIKE ?
            LIMIT 10
    ''', conn, params=(txtsearch_fix, txtsearch_fix))
    return songs

def get_song(conn, song_id):
    songs = pandas.read_sql_query('''
                                  SELECT * FROM songs WHERE song_id = ?
                                  ''', conn, params=(song_id,))
    return songs.head(1)

def get_all_trackings(conn):
    trackings = pandas.read_sql_query('''
                                  SELECT * FROM trackings
                                  ''', conn)
    return trackings

def check_login(conn, user_id, password):
    print(user_id)
    print(password)
    users = pandas.read_sql_query('''
                                SELECT * FROM users WHERE user_id = ? AND password = ?
                                ''', conn, params=[user_id, password])
    if users.empty:
        return {'success': False}
    return {'success': True, 'user': users.head(1)}
