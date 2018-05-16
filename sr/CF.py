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
song_df_1 = song_df_1.rename(columns={'timestamp': 'listen_count'})

# tracking_file = 'Dataset/Test/10000_line.txt'
# songs_metadata_file = 'Dataset/Test/song_data.csv'

# song_df_1 = pd.read_table(tracking_file, delim_whitespace=True, header=None)
# song_df_1.columns = ['user_id', 'song_id', 'listen_count']

# song_df_2 = pd.read_csv(songs_metadata_file)

# song_df = pd.merge(song_df_1, song_df_2.drop_duplicates(['song_id']), on="song_id", how="left")

users_unique = song_df_1['user_id'].unique()
items_unique = song_df_1['song_id'].unique()

# *** Gợi ý theo mức độ phổ biến ***
# rs = Recommenders.popularity_recommender()
# rs.create(song_df_1, 'user_id', 'song_id')
# recommendation_songs_rank = rs.recommend(users[0])
# recommendation_songs_id = recommendation_songs_rank['song_id']
# recommendation_songs_data = songs.query("song_id in @recommendation_songs_id")
# recommendation = pd.merge(recommendation_songs_rank, recommendation_songs_data.drop_duplicates(['song_id']), on="song_id", how="left")
# **********************************

num_users = len(users_unique)
num_songs = len(items_unique)

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
mt_user = df_user.as_matrix()

df_item = pd.DataFrame([id_item_current, index_items_unique]).T
df_item.columns = ["item_id", "index"]
mt_item = df_item.as_matrix()

rs = Recommenders.collaborative_filtering()

# uu_CF = 1 là user-user, 0 là item-item
uu_CF = 1
# Số kết quả trả về
num_result = 10

rs.create(Ybar_data, k = 2, dist_func = cosine_similarity, uuCF = uu_CF, n_users = num_users, n_items = num_songs)

# normalize và tính toán độ tương đồng
rs.fit()

# Đưa ra gợi ý với tất cả các user
# rs.print_recommendation_all(num_result)

# Đưa ra gợi ý với user đầu vào

list_item_id = []
if(uu_CF):
    id_user = str(sys.argv[1])
    index_user = mt_user[mt_user[:, 0] == id_user][0][1]
    list_index = rs.print_recommendation_with_index(index_user, num_result)

    for i in list_index:
        list_item_id.append(mt_item[mt_item[:, 1] == i][0][0])

    recommendation_songs_data = songs.query("song_id in @list_item_id")

    print(recommendation_songs_data)
    print(type(recommendation_songs_data))
else:
    id_item = str(sys.argv[1])
    index_item = mt_item[mt_item[:, 0] == id_item][0][1]
    list_index = rs.print_recommendation_with_index(index_item, num_result)

    for i in list_index:
        list_item_id.append(mt_user[mt_user[:, 1] == i][0][0])

    recommendation_users_data = users.query("user_id in @list_item_id")

    print(recommendation_users_data)

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