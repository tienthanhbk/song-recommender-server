import QueryPool
import os
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import sys
import Recommenders

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
# Fix path to database file under here
DB_URI = os.path.join(CURRENT_PATH, 'db', 'recommender.db')
# Fix path to database file upon here
conn = QueryPool.create_connection(DB_URI)

users = QueryPool.get_all_users(conn)
songs = QueryPool.get_all_songs(conn)
trackings = QueryPool.get_all_trackings(conn)

song_df_1 = trackings.groupby(['user_id', 'song_id']).agg({'timestamp': 'count'}).reset_index()

# tracking_file = 'Dataset/Test/10000_line.txt'
# songs_metadata_file = 'Dataset/Test/song_data.csv'

# song_df_1 = pd.read_table(tracking_file, delim_whitespace=True, header=None)
# song_df_1.columns = ['user_id', 'song_id', 'listen_count']

# song_df_2 = pd.read_csv(songs_metadata_file)

# song_df = pd.merge(song_df_1, song_df_2.drop_duplicates(['song_id']), on="song_id", how="left")

users = song_df_1['user_id'].unique()
items = song_df_1['song_id'].unique()

# *** Gợi ý theo mức độ phổ biến ***
rs = Recommenders.popularity_recommender()
rs.create(song_df_1, 'user_id', 'song_id')
recommendation_songs_id = rs.recommend(users[0])
recommendation_songs_data = songs.query("song_id in @recommendation_songs_id")
print(recommendation_songs_data)
# **********************************

# num_users = len(users)
# num_songs = len(items)

# Y_data = song_df_1.as_matrix()
# Ybar_data = Y_data.copy()

# ids_user = []
# ids_item = []
# count = []
# id_user_current = []
# id_item_current = []
# i = 0
# j = 0

# for id_user, id_song, listen_count in Ybar_data:
#     if id_user in id_user_current:
#         ids_user.append(id_user_current.index(id_user))
#     else:
#         ids_user.append(i)
#         i = i + 1
#         id_user_current.append(id_user)
#     if id_song in id_item_current:
#         ids_item.append(id_item_current.index(id_song))
#     else:
#         ids_item.append(j)
#         j = j + 1
#         id_item_current.append(id_song)
#     count.append(listen_count)

# Ybar_data[:, 0] = ids_user
# Ybar_data[:, 1] = ids_item
# Ybar_data[:, 2] = count

# rs = Recommenders.collaborative_filtering()

# rs.create(Ybar_data, k = 2, dist_func = cosine_similarity, uuCF = 1, n_users = num_users, n_items = num_songs)

# normalize và tính toán độ tương đồng
# rs.fit()

# Đưa ra gợi ý với tất cả các user
# rs.print_recommendation_all()

# Đưa ra gợi ý với user đầu vào
# index = int(sys.argv[1])
# rs.print_recommendation_with_index(index)

# *****************************************
# r_cols = ['user_id', 'item_id', 'rating']

# rating = pd.read_csv('ex.dat', sep = ' ', names = r_cols, encoding = 'latin-1')

# Y_data = rating.as_matrix()

# rs = CF(Y_data, k = 2, uuCF = 0)
# rs.fit()

# rs.print_recommendation()

# r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']

# ratings_base = pd.read_csv('ml-100k/ub.base', sep='\t', names=r_cols, encoding='latin-1')
# ratings_test = pd.read_csv('ml-100k/ub.test', sep='\t', names=r_cols, encoding='latin-1')

# rate_train = ratings_base.as_matrix()
# rate_test = ratings_test.as_matrix()

# # indices start from 0
# rate_train[:, :2] -= 1
# rate_test[:, :2] -= 1

# rs = CF(rate_train, k = 30, uuCF = 1)
# rs.fit()

# n_tests = rate_test.shape[0]
# SE = 0 # squared error
# for n in range(n_tests):
#     pred = rs.pred(rate_test[n, 0], rate_test[n, 1], normalized = 0)
#     SE += (pred - rate_test[n, 2])**2

# RMSE = np.sqrt(SE/n_tests)
# print('User-user CF, RMSE =', RMSE)

