import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse

class user():
    def __init__(self):
        super(ClassName, self).__init__()
        self.arg = arg

class popularity_recommender():
    def __init__(self):
        self.train_data = None
        self.user_id = None
        self.item_id = None
        self.popularity_recommendations = None

    #Create the popularity based recommender system model
    def create(self, train_data, user_id, item_id):
        self.train_data = train_data
        self.user_id = user_id
        self.item_id = item_id

        # Nhóm theo item_id
        train_data_grouped = train_data.groupby([self.item_id]).agg({self.user_id: 'count'}).reset_index()
        # Score của mỗi item_id chính bằng tổng số user_id nghe bài hát đấy
        train_data_grouped.rename(columns = {'user_id': 'score'},inplace=True)

        # Sắp xếp tập train_data theo score
        train_data_sort = train_data_grouped.sort_values(['score', self.item_id], ascending = [0,1])

        # Tạo một cái đề xuất xếp hạng dựa trên score
        train_data_sort['Rank'] = train_data_sort['score'].rank(ascending=0, method='first')

        # Lấy ra 10 cái đầu tiên trong danh sách xếp hạng
        self.popularity_recommendations = train_data_sort.head(10)

    #Use the popularity based recommender system model to make recommendations
    def recommend(self, user_id):
        user_recommendations = self.popularity_recommendations

        # Thêm cột user_id vào trong danh sách gợi ý
        user_recommendations['user_id'] = user_id

        # Lấy ra danh sách các cột
        cols = user_recommendations.columns.tolist()
        # Đưa user_id cột lên đầu
        cols = cols[-1:] + cols[:-1]

        user_recommendations = user_recommendations[cols]

        return user_recommendations

class collaborative_filtering():
    def __init__(self):
        self.uuCF = None
        self.Y_data = None
        self.k = None
        self.dist_func = None
        self.Ybar_data = None
        self.n_users = None
        self.n_items = None

    def create(self, Y_data, k, dist_func, uuCF, n_users, n_items):
        self.uuCF = uuCF
        self.Y_data = Y_data if uuCF else Y_data[:, [1, 0, 2]]
        self.k = k
        self.dist_func = dist_func

        # Số lượng user và item
        self.n_users = n_users if uuCF else n_items
        self.n_items = n_items if uuCF else n_users

    def add(self, new_data):
        self.Y_data = np.concatenate((self.Y_data, new_data), axis = 0)

    def normalize_Y(self):
        users = self.Y_data[:, 0]
        self.Ybar_data = self.Y_data.copy()
        self.mu = np.zeros((self.n_users,))
        # Với từng user
        for n in range(self.n_users):
            ids = np.where(users == n)[0].astype(np.int32)
            # Lấy ra danh sách id của item
            item_ids = self.Y_data[ids, 1]
            # Lấy ra đánh gía
            ratings = self.Y_data[ids, 2]
            # Tính trung bình các đánh gía của user
            self.mu[n] = np.mean(ratings)

            # Xây dựng ma trận xếp hạng dưới dạng ma trận thưa
            # Chỉ lưu trữ vị trí của nó thay vì lưu trữ toàn bộ ma trận item*user
            self.Ybar_data[ids, 2] = ratings - self.mu[n]
        self.Ybar = sparse.coo_matrix((np.array(self.Ybar_data[:, 2], dtype=np.float32),
            (self.Ybar_data[:, 1], self.Ybar_data[:, 0])), shape=(self.n_items, self.n_users))
        self.Ybar = self.Ybar.tocsr()

    def similarity(self):
        # Tính toán độ tương đồng, Ybar.T là ma trận chuyển vị của ma trận Ybar
        self.S = self.dist_func(self.Ybar.T, self.Ybar.T)

    def fit(self):
        self.normalize_Y()
        self.similarity()

    def __pred(self, u, i, normalized = 1):
        ids = np.where(self.Y_data[:, 1] == i)[0].astype(np.int32)
        # Các user đã rate item i
        users_rated_i = (self.Y_data[ids, 0]).astype(np.int32)
        # Mảng độ tương đồng giữa các user
        sim = self.S[u, users_rated_i]

        # Lấy ra k kết quả lớn nhất
        a = np.argsort(sim)[-self.k:]
        nearest_s = sim[a]

        r = self.Ybar[i, users_rated_i[a]]
        if normalized:
            return (r*nearest_s)[0]/(np.abs(nearest_s).sum() + 1e-8)
        return (r*nearest_s)[0]/(np.abs(nearest_s).sum() + 1e-8) + self.mu[u]

    def pred(self, u, i, normalized = 1):
        if self.uuCF: return self.__pred(u, i)
        return self.__pred(u, i)

    def recommend(self, u, normalized = 1):
        ids = np.where(self.Y_data[:, 0] == u)[0]
        items_rated_by_u = self.Y_data[ids, 1].tolist()
        recommended_items = []
        for i in range(self.n_items):
            if i not in items_rated_by_u:
                rating = self.pred(u, i)
                if rating > 0:
                    recommended_items.append(i)
        return recommended_items

    def print_recommendation_all(self):
        for u in range(self.n_users):
            recommended_items = self.recommend(u)
            if self.uuCF:
                print('    Recommend item(s):', recommended_items, 'to user', u)
            else:
                print('    Recommend item', u, 'to user(s) : ', recommended_items)

    def print_recommendation_with_index(self, u):
        recommended_items = self.recommend(u)
        if self.uuCF:
            print('    Recommend item(s):', recommended_items, 'to user', u)
        else:
            print('    Recommend item', u, 'to user(s) : ', recommended_items)