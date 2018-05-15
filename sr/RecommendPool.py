import QueryPool
import os
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import sys
import Recommenders

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
DB_URI = os.path.join(CURRENT_PATH, 'db', 'recommender.db')

def get_top_songs(conn):
  users = QueryPool.get_all_users(conn)
  songs = QueryPool.get_all_songs(conn)
  trackings = QueryPool.get_all_trackings(conn)
  
  song_df_1 = trackings.groupby(['user_id', 'song_id']).agg({'timestamp': 'count'}).reset_index()

  users = song_df_1['user_id'].unique()
  items = song_df_1['song_id'].unique()

  rs = Recommenders.popularity_recommender()
  rs.create(song_df_1, 'user_id', 'song_id')
  recommendation_songs_id = rs.recommend(users[0])
  recommendation_songs_data = songs.query("song_id in @recommendation_songs_id")

  return recommendation_songs_data
