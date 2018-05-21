# -*- coding: utf-8 -*-

# Create smaller data
import pandas
import os

#Get currect directory
DIR_PATH = os.path.abspath(os.path.dirname(__file__))

#Sua lai duong dan o day
TRACKING_FILE_PATH = DIR_PATH + '/data/song-tracking.csv'
SONG_FILE_PATH = DIR_PATH + '/data/song.csv'
SONG_POPULAR_FILE_PATH = DIR_PATH + '/data/popular-song.csv'
USER_FILE_PATH = DIR_PATH + '/data/user.csv'
DATA_SAMPLE_STORED_PATH = DIR_PATH + '/data-sample'
#Sua lai duong dan tren day

# Create directory if not exists
if not os.path.exists(DATA_SAMPLE_STORED_PATH):
    os.makedirs(DATA_SAMPLE_STORED_PATH)

tracking_file = open(TRACKING_FILE_PATH, 'r')
song_file = open(SONG_FILE_PATH, 'r')
popular_song_file = open(SONG_POPULAR_FILE_PATH)
user_file = open(USER_FILE_PATH, 'r')

tracking_df = pandas.read_csv(tracking_file,
    header=0,
    # nrows=10000,
    error_bad_lines=False)

song_df = pandas.read_csv(song_file,
    header=0,
    error_bad_lines=False)
user_df = pandas.read_csv(user_file,
    header=0,
    error_bad_lines=False)
song_popular_df = pandas.read_csv(popular_song_file,
    header=0,
    error_bad_lines=False)

top_song_popular = song_popular_df.head(500)
id_top_song = top_song_popular['song_id']


# tracking_sample_df = tracking_df.sample(n=10000, random_state=16)
tracking_sample_df = tracking_df[tracking_df['song_id'].isin(id_top_song)]
song_sample_df = tracking_sample_df.drop_duplicates(['song_id']).filter(['song_id', 'song_name', 'artist_name'], axis=1)
user_sample_df = tracking_sample_df.drop_duplicates(['user_id']).filter(['user_id'], axis=1)

user_sample_df['password'] = user_sample_df['user_id']

tracking_sample_df.to_csv(DATA_SAMPLE_STORED_PATH + '/tracking_sample.csv',
                          encoding='utf-8',
                          index=False)
song_sample_df.to_csv(DATA_SAMPLE_STORED_PATH + '/song_sample.csv',
                      encoding='utf-8',
                      index=False)
user_sample_df.to_csv(DATA_SAMPLE_STORED_PATH + '/user_sample.csv',
                      encoding='utf-8',
                      index=False)

# Lay ra 3000 bai hat nghe nhieu nhat: song_id, song_name, artist_name
# lay id 3000 bai do
# lay ra cac trackings cua cac bai hat do: df[df['song_id'].isin([array_song_id])]
# user giu nguyen (1k user)





