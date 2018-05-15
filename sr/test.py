import pandas
import query_pool
import os

DIR_PATH = os.path.abspath(os.path.dirname(__file__))
DB_STORED_PATH = os.path.join(DIR_PATH, 'db')
DB_URI = os.path.join(DB_STORED_PATH, 'recommender.db')

test = pandas.DataFrame({'name': ['a', 'b'], 'age': [12, 13]})

conn = query_pool.create_connection(DB_URI)
login_return = query_pool.check_login(conn, 'user_000005', 'user_000005')


