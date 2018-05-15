import pandas
import QueryPool
import os

DIR_PATH = os.path.abspath(os.path.dirname(__file__))
DB_STORED_PATH = os.path.join(DIR_PATH, 'db')
DB_URI = os.path.join(DB_STORED_PATH, 'recommender.db')

test = pandas.DataFrame({'name': ['a', 'b'], 'age': [12, 13]})

conn = QueryPool.create_connection(DB_URI)
login_return = QueryPool.check_login(conn, 'user_000005', 'user_000005')


