import QueryPool
import os
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import sys
import Recommenders

import time
import datetime

class CF():
    def __init__(self):
        # super(CF, self).__init__()
        self.CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
        # Fix path to database file under here
        self.DB_URI = os.path.join(self.CURRENT_PATH, 'db', 'recommender.db')
        # Fix path to database file upon here
        self.conn = QueryPool.create_connection(self.DB_URI)

        # Lấy ra danh sách users, songs, trackings từ db
        self.users = QueryPool.get_all_users(self.conn)
        self.songs = QueryPool.get_all_songs(self.conn)
        self.trackings = QueryPool.get_all_trackings(self.conn)

        self.process_df()

    def add_tracking_file(self, user_id, item_id):
        # *********************************
        # User nghe thêm bài hát khát
        # Lấy thời gian hiện tại
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%SZ')

        # Tạo bản ghi mới
        df_record_tracking = pd.DataFrame([user_id, item_id, st]).T
        df_record_tracking.columns = ["user_id", "song_id", "timestamp"]
        df_record_tracking.index = [len(self.trackings)]

        # Thêm bản ghi mới vào file trackings
        self.trackings = pd.concat([self.trackings,df_record_tracking],axis=0)

        self.process_df()
        # **********************************

    def process_df(self):
        self.song_df_1 = self.trackings.groupby(['user_id', 'song_id']).agg({'timestamp': 'count'}).reset_index()
        self.song_df_1 = self.song_df_1.rename(columns={'timestamp': 'listen_count'})
        users = self.song_df_1['user_id'].unique()
        items = self.song_df_1['song_id'].unique()
        self.num_users = len(users)
        self.num_items = len(items)

    def popularity_recommender(self):
        self.rs = Recommenders.popularity_recommender()
        self.rs.create(self.song_df_1, 'user_id', 'song_id')
        recommendation_songs_rank = self.rs.recommend()
        recommendation_songs_id = recommendation_songs_rank['song_id']
        recommendation_songs_data = self.songs.query("song_id in @recommendation_songs_id")
        recommendation = pd.merge(recommendation_songs_rank, recommendation_songs_data.drop_duplicates(['song_id']), on="song_id", how="left")
        return recommendation

    def create_matrix(self):
        self.Y_data = self.song_df_1.as_matrix()

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

        for id_user, id_song, listen_count in self.Y_data:
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

        self.Y_data[:, 0] = index_users
        self.Y_data[:, 1] = index_items
        self.Y_data[:, 2] = count

        self.df_user = pd.DataFrame([id_user_current, index_users_unique]).T
        self.df_user.columns = ["user_id", "index"]
        self.mt_user = self.df_user.as_matrix()

        self.df_item = pd.DataFrame([id_item_current, index_items_unique]).T
        self.df_item.columns = ["item_id", "index"]
        self.mt_item = self.df_item.as_matrix()

    def collaborative_filtering(self, uu_CF, num_result, id):
        self.rs = Recommenders.collaborative_filtering()

        self.rs.create(self.Y_data, k = 2, dist_func = cosine_similarity, uuCF = uu_CF, n_users = self.num_users, n_items = self.num_items)

        # normalize và tính toán độ tương đồng
        self.rs.fit()

        if not id:
            # Đưa ra gợi ý với tất cả các user
            self.rs.print_recommendation_all(num_result)
        else:
            list_item_id = []
            if(uu_CF):
                index_user = self.mt_user[self.mt_user[:, 0] == id][0][1]
                list_index = self.rs.print_recommendation_with_index(index_user, num_result)

                list_item_id = self.get_item_id_by_index(list_index)

                recommendation_songs_data = self.songs.query("song_id in @list_item_id")
            else:
                index_item = self.mt_item[self.mt_item[:, 0] == id][0][1]
                list_index = self.rs.print_recommendation_with_index(index_item, num_result)

                list_item_id = self.get_user_id_by_index(list_index)

                recommendation_users_data = self.users.query("user_id in @list_item_id")

    def get_user_id_by_index(self, index):
        list_item_id = []
        for i in index:
            list_item_id.append(self.mt_user[self.mt_user[:, 1] == i][0][0])
        return list_item_id

    def get_item_id_by_index(self, index):
        list_item_id = []
        for i in index:
            list_item_id.append(self.mt_item[self.mt_item[:, 1] == i][0][0])
        return list_item_id

test = CF()
test.create_matrix()
test.collaborative_filtering(uu_CF = 1, num_result = 10, id = "user_000008")

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