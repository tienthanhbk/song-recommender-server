# Nomalize origin data
import pandas
import os

# Get currect directory
DIR_PATH = os.path.abspath(os.path.dirname(__file__))

# Sua lai duong dan o day
DATASET_PATH = DIR_PATH + '/data-origin/lastfm-dataset-1K/userid-timestamp-artid-artname-traid-traname.tsv'
DATA_STORED_PATH = DIR_PATH + '/data' # Thu muc ma du lieu se duoc luu thanh file csv
# Sua lai duong dan tren day

# Create directory if not exists
if not os.path.exists(DATA_STORED_PATH):
    os.makedirs(DATA_STORED_PATH)

dataset_file = open(DATASET_PATH, 'r')

dataset_df = pandas.read_table(
    dataset_file,
    header=None,
#    nrows=50000,
    names=['user_id', 'timestamp', 'artist_id', 'artist_name', 'song_id', 'song_name'],
    usecols=['user_id', 'timestamp', 'artist_name', 'song_id', 'song_name'],
    error_bad_lines=False)

dataset_df = dataset_df.dropna(subset=['song_id'])
count_nan = dataset_df.isnull().sum()

user_df = dataset_df.drop_duplicates(['user_id']).filter(['user_id'], axis=1)
song_df = dataset_df.drop_duplicates(['song_id']).filter(['song_id', 'song_name', 'artist_name'], axis=1)

dataset_df.to_csv(DATA_STORED_PATH + '/song-tracking.csv', encoding='utf-8', index=False)
user_df.to_csv(DATA_STORED_PATH + '/user.csv', encoding='utf-8', index=False)
song_df.to_csv(DATA_STORED_PATH + '/song.csv', encoding='utf-8', index=False)

dataset_file.close()



