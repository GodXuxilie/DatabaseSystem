import pymysql
import pandas as pd
import pickle
import numpy as np
import databaseInfo as db

databaseName = 'root'
databasePasswd = 'root'

def user_info_query(user_id):
    conn = pymysql.connect(host=db.databaseAddress, user=db.databaseLoginName, password=db.databasePasswd, database=db.databaseName)
    cur = conn.cursor()
    users = pd.read_sql("select * from User", conn)
    users = users.filter(regex='UserID|Gender|Age|JobID')

    # 改变User数据中性别和年龄
    gender_map = {'F': 0, 'M': 1}
    users['Gender'] = users['Gender'].map(gender_map)

    age_map = {val: ii for ii, val in enumerate(set(users['Age']))}
    users['Age'] = users['Age'].map(age_map)
    users_list = users.values
    # print(users.head())
    cur.close()  # 归还资源
    conn.close()
    num_line = 0
    for index in range(len(users_list)):
        if int(users_list[index][0]) == user_id:
            num_line = index
            break
    #return users_list[user_id-1][0],users_list[user_id-1][1],users_list[user_id-1][2],users_list[user_id-1][3]
    return users_list[num_line][0],users_list[num_line][1],users_list[num_line][2],users_list[num_line][3]

# print(user_info_query(4))

def movie_info_query(user_id):
    conn = pymysql.connect(host=db.databaseAddress, user=db.databaseLoginName, password=db.databasePasswd, database=db.databaseName)
    cur = conn.cursor()
    title_count, title_set, genres2int, features, targets_values, ratings, users, movies, data, movies_orig, users_orig = pickle.load(
        open('preprocess.p', mode='rb'))
    sentences_size = title_count
    # 电影ID转下标的字典，数据集中电影ID跟下标不一致，比如第5行的数据电影ID不一定是5
    movieid2idx = {val[0]: i for i, val in enumerate(movies.values)}

    movies_id_list = pd.read_sql("select MovieID from watch_history where UserID={}".format(user_id), conn)
    # print(movies.head())
    movies_id_list = movies_id_list.values
    # print(movies_id_list)
    history_movie_feature_list = []
    for i in range(len(movies_id_list)):
        movie_feature = []
        movie_id_val = movies_id_list[i][0]
        # print(movie_id_val)
        categories = np.zeros([1, 18])
        categories[0] = movies.values[movieid2idx[movie_id_val]][2]
        titles = np.zeros([1, sentences_size])
        titles[0] = movies.values[movieid2idx[movie_id_val]][1]
        movie_id = np.reshape(movies.values[movieid2idx[movie_id_val]][0], [1])
        movie_categories = categories
        movie_titles = titles
        movie_feature.append(movie_id)
        movie_feature.append(movie_categories)
        movie_feature.append(movie_titles)
        history_movie_feature_list.append(movie_feature)
    cur.close()  # 归还资源
    conn.close()
    return history_movie_feature_list

# print(movie_info_query(1))


