# -*- coding: utf-8 -*-

import QueryPool
import os

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
# Fix path to database file under here
DB_URI = os.path.join(CURRENT_PATH, 'db', 'recommender.db')
# Fix path to database file upon here

conn = QueryPool.create_connection(DB_URI)

users = QueryPool.get_all_users(conn)
songs = QueryPool.get_all_songs(conn)
trackings = QueryPool.get_all_trackings(conn)
