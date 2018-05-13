# -*- coding: utf-8 -*-

# Set data to sql db
import os
import sqlite3
from sqlite3 import Error
import pandas

#Get currect directory
DIR_PATH = os.path.abspath(os.path.dirname(__file__))

#Sua lai duong dan o day
DATA_STORED_PATH = DIR_PATH + '/data'
DB_STORED_PATH = DIR_PATH + '/db'
DATA_SAMPLE_STORED_PATH = DIR_PATH + '/data-sample'
#Sua lai duong dan tren day

# Create directory if not exists
if not os.path.exists(DB_STORED_PATH):
    os.makedirs(DB_STORED_PATH)


def get_data_from_csv(path, header=0):
    """ Read data from file
    :param path: Path to csv file
    :return: DataFrame
    """
    file = open(path)
    frame = pandas.read_csv(file, header=header, error_bad_lines=False)
    return frame
    
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

def drop_exist_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
        DROP TABLE IF EXISTS 'songs'
    ''')
    cursor.execute('''
        DROP TABLE IF EXISTS 'users'
    ''')
    cursor.execute('''
        DROP TABLE IF EXISTS 'trackings'
    ''')
    conn.commit()
    
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE users 
        (user_id text)
    ''')
    cursor.execute('''
        CREATE TABLE songs 
        (song_id text, song_name text, artist_name text)
    ''')
    cursor.execute('''
        CREATE TABLE trackings 
        (user_id text, song_id text, timestamp text) 
    ''')

def append_data_to_db(conn, data_df, table_name):
    data_df.to_sql(name=table_name, con=conn, if_exists="append", index=False)


conn = create_connection(DB_STORED_PATH + '/recommender.db')
cursor = conn.cursor()
drop_exist_tables(conn)
create_table(conn)

song_df = get_data_from_csv(DATA_SAMPLE_STORED_PATH + '/song_sample.csv')
tracking_df = get_data_from_csv(DATA_SAMPLE_STORED_PATH + '/tracking_sample.csv')
user_df = get_data_from_csv(DATA_STORED_PATH + '/user.csv')

append_data_to_db(conn, song_df, 'songs')
append_data_to_db(conn, tracking_df[['user_id', 'song_id', 'timestamp']], 'trackings')
append_data_to_db(conn, user_df, 'users')



