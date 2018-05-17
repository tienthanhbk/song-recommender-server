import pandas
import QueryPool
import os

DIR_PATH = os.path.abspath(os.path.dirname(__file__))
DB_STORED_PATH = os.path.join(DIR_PATH, 'db')
DB_URI = os.path.join(DB_STORED_PATH, 'recommender.db')
TRACKING_FILE_PATH = DIR_PATH + '/data/song-tracking.csv'
SONG_FILE_PATH = DIR_PATH + '/data/song.csv'
song_file = open(SONG_FILE_PATH, 'r')

tracking_file = open(TRACKING_FILE_PATH, 'r')
song_df = pandas.read_csv(song_file,
                          header=0,
                          error_bad_lines=False)

tracking_df = pandas.read_csv(tracking_file,
                              header=0,
#                              nrows=100000,
                              error_bad_lines=False)
#tracking_sample_df = tracking_df.sample(n=10000, random_state=16)

listen_info_df = tracking_df.drop_duplicates(['user_id', 'song_id']).filter(['user_id', 'song_id'], axis=1).groupby(['song_id']).agg({'user_id': 'count'}).reset_index()
listen_info_df = listen_info_df.rename(columns={'user_id': 'user_listen'})

popular_songs = listen_info_df.sort_values(by='user_listen', ascending=False)
