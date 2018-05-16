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

def get_recommend_songs(conn, user_id):
  users = QueryPool.get_all_users(conn)
  songs = QueryPool.get_all_songs(conn)

  trackings = QueryPool.get_all_trackings(conn)
  song_df_1 = trackings.groupby(['user_id', 'song_id']).agg({'timestamp': 'count'}).reset_index()
  
  users = song_df_1['user_id'].unique()
  items = song_df_1['song_id'].unique()

  num_users = len(users)
  num_songs = len(items)

  Y_data = song_df_1.as_matrix()
  Ybar_data = Y_data.copy()

  index_users = []
  index_users_unique = []
  index_items = []
  index_items_unique = []
  count = []
  id_user_current = []
  id_item_current = []
  list_user = []
  i = 0
  j = 0

  for id_user, id_song, listen_count in Ybar_data:
    if id_user in id_user_current:
        index_users.append(id_user_current.index(id_user))
    else:
        index_users.append(i)
        index_users_unique.append(i)
        i = i + 1
        id_user_current.append(id_user)
    list_user.append(Recommenders.user(id_user_current.index(id_user), id_user))
    if id_song in id_item_current:
        index_items.append(id_item_current.index(id_song))
    else:
        index_items.append(j)
        index_items_unique.append(j)
        j = j + 1
        id_item_current.append(id_song)
    count.append(listen_count)

  Ybar_data[:, 0] = index_users
  Ybar_data[:, 1] = index_items
  Ybar_data[:, 2] = count

  df_user = pd.DataFrame([id_user_current, index_users_unique]).T
  df_user.columns = ["user_id", "index"]

  df_item = pd.DataFrame([id_item_current, index_items_unique]).T
  df_item.columns = ["item_id", "index"]

  rs = Recommenders.collaborative_filtering()

  rs.create(Ybar_data, k = 2, dist_func = cosine_similarity, uuCF = 1, n_users = num_users, n_items = num_songs)
  
  # normalize và tính toán độ tương đồng
  rs.fit()

  # Đưa ra gợi ý với user đầu vào
  index = 6
  list_index = rs.print_recommendation_with_index(index)
  list_item_id = []
  for i in list_index:
      list_item_id.append(df_item.ix[i,"item_id"])
  recommendation_songs_data = songs.query("song_id in @list_item_id")
  print(recommendation_songs_data)
  return recommendation_songs_data
