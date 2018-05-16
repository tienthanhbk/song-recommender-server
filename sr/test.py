import pandas
import QueryPool
import os

DIR_PATH = os.path.abspath(os.path.dirname(__file__))
DB_STORED_PATH = os.path.join(DIR_PATH, 'db')
DB_URI = os.path.join(DB_STORED_PATH, 'recommender.db')
TRACKING_FILE_PATH = DIR_PATH + '/data/song-tracking.csv'

tracking_file = open(TRACKING_FILE_PATH, 'r')

tracking_df = pandas.read_csv(tracking_file,
                              header=0,
#                              nrows=100000,
                              error_bad_lines=False)
tracking_sample_df = tracking_df.sample(n=10000, random_state=16)

listen_count = tracking_sample_df.drop_duplicates(['user_id', 'song_id']).filter(['user_id', 'song_id'], axis=1).groupby(['song_id']).agg({'user_id': 'count'}).reset_index()
songs_popular = listen_count.groupby(['song_id']).agg({'user_id': 'count'}).reset_index()
count1 = listen_count['user_id'].sum()
count2 = songs_popular['user_id'].sum()