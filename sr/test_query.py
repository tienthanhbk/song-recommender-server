# -*- coding: utf-8 -*-

import query_pool
import os

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
# Fix path to database file under here
DB_URI = os.path.join(CURRENT_PATH, 'db', 'recommender.db')
# Fix path to database file upon here

conn = query_pool.create_connection(DB_URI)

users = query_pool.get_all_users(conn)
songs = query_pool.get_all_songs(conn)
trackings = query_pool.get_all_trackings(conn)
