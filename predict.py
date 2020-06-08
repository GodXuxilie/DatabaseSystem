import os
from model import *
from mysql_operation import *
import random

seed = 1
torch.manual_seed(seed)
np.random.seed(seed)
torch.cuda.manual_seed_all(seed)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

model_dir = './movie_recommendation_model'
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

title_count, title_set, genres2int, features, targets_values, ratings, users, movies, data, movies_orig, users_orig = pickle.load(open('preprocess.p', mode='rb'))

embed_dim = 32
uid_max = max(features.take(0,1)) + 1
gender_max = max(features.take(2,1)) + 1
age_max = max(features.take(3,1)) + 1
job_max = max(features.take(4,1)) + 1
movie_id_max = max(features.take(1,1)) + 1
movie_categories_max = max(genres2int.values()) + 1
movie_title_max = len(title_set)
sentences_size = title_count
# print(uid_max,gender_max,age_max,job_max,movie_id_max,movie_title_max,movie_categories_max)

#电影ID转下标的字典，数据集中电影ID跟下标不一致，比如第5行的数据电影ID不一定是5
movieid2idx = {val[0]:i for i, val in enumerate(movies.values)}

model = MR_Model(uid_max, gender_max, age_max, job_max, movie_id_max, movie_categories_max, movie_title_max)
model_dir = './movie_recommendation_model'
pt_name = model_dir + '/lr_checkpoint.pt'
model.load_state_dict(torch.load(pt_name, map_location="cpu"))

def rating_movie(user_id_val, movie_id_val):
    model.eval()
    categories = np.zeros([1, 18])
    categories[0] = movies.values[movieid2idx[movie_id_val]][2]
    titles = np.zeros([1, sentences_size])
    titles[0] = movies.values[movieid2idx[movie_id_val]][1]

    users_list = users.values
    num_line = 0
    for index in range(len(users_list)):
        if int(users_list[index][0]) == user_id_val:
            num_line = index
            break

    uid = np.reshape(users_list[num_line][0], [1])
    user_gender = np.reshape(users_list[num_line][1], [1])
    user_age = np.reshape(users_list[num_line][2], [1])
    user_job = np.reshape(users_list[num_line][3], [1])
    movie_id = np.reshape(movies.values[movieid2idx[movie_id_val]][0], [1])
    movie_categories = categories
    movie_titles = titles
    # print(features[0])
    # print(uid,user_gender,user_age,user_job,movie_id,movie_categories,movie_titles)
    uid, user_gender, user_age, user_job, movie_id, movie_categories, movie_titles = torch.LongTensor(uid),torch.LongTensor(user_gender)\
        ,torch.LongTensor(user_age),torch.LongTensor(user_job),torch.LongTensor(movie_id),torch.LongTensor(movie_categories),torch.LongTensor(movie_titles)
    # print(uid.shape, user_gender.shape, user_age.shape, user_job.shape, movie_id.shape, movie_categories.shape,
    #       movie_titles.shape)
    user_feature, movie_feature, rating = model(uid, user_gender, user_age, user_job, movie_id, movie_categories,
                                                movie_titles)
    return rating.data

# print(rating_movie(2,1193))

def recommend_same_type_movie(movie_id_val, top_k = 60):
    movie_matrics = pickle.load(open('movie_matrics.p', mode='rb'))
    probs_embeddings = (movie_matrics[movieid2idx[movie_id_val]]).reshape([200, 1])
    sim = np.dot(movie_matrics, probs_embeddings)
    # print(probs.shape)
    # print("您看的电影是：{}".format(movies_orig[movieid2idx[movie_id_val]]))
    # print("以下是给您的推荐：")
    p = np.squeeze(sim)
    p[np.argsort(p)[:-top_k]] = 0
    p = p / np.sum(p)
    results = set()
    while len(results) != top_k//2:
        c = np.random.choice(3883, 1, p=p)[0]
        if movies_orig[c][0] != movie_id_val:
            results.add(c)
    # for val in (results):
    #     print(val)
    #     print(movies_orig[val])
    return results

# recommend_same_type_movie(4)

def recommend_your_favorite_movie(user_id_val, top_k=60):
    history_movie = movie_info_query(user_id_val)
    user_info = user_info_query(user_id_val)
    same_type_history_movie = []
    for i in range(len(history_movie)):
        result = recommend_same_type_movie(history_movie[i][0][0])
        for x in result:
            same_type_history_movie.append(x)

    sim = []
    for item in movies.values:
        movies_id = item.take(0)
        rating = rating_movie(user_id_val,movie_id_val=movies_id)
        if same_type_history_movie.__contains__(item[0]):
            rating *= 5
        sim.append(rating)

    #print("UserID{} 以下是给您的推荐：".format(user_id_val))
    p = np.squeeze(sim)
    p[np.argsort(p)[:-top_k]] = 0
    p = p / np.sum(p)
    results = set()
    while len(results) != top_k//2:
        c = np.random.choice(3883, 1, p=p)[0]
        results.add(c)
    #for val in (results):
        #print(val)
        #print(movies_orig[val])
    return results

#recommend_your_favorite_movie(1)
#recommend_your_favorite_movie(2)
#recommend_your_favorite_movie(234)




def recommend_other_favorite_movie(movie_id_val, top_k=60):
    movie_matrics = pickle.load(open('movie_matrics.p', mode='rb'))
    users_matrics = pickle.load(open('user_matrics.p', mode='rb'))
    probs_movie_embeddings = (movie_matrics[movieid2idx[movie_id_val]]).reshape([200, 1])
    probs_user_favorite_similarity = np.dot(movie_matrics,probs_movie_embeddings)
    favorite_user_id = np.argsort(probs_user_favorite_similarity)[0][-top_k:]
    #     print(normalized_users_matrics.eval().shape)
    #     print(probs_user_favorite_similarity.eval()[0][favorite_user_id])
    #     print(favorite_user_id.shape)

    print("您看的电影是：{}".format(movies_orig[movieid2idx[movie_id_val]]))

    print("喜欢看这个电影的人是：{}".format(users_orig[favorite_user_id - 1]))
    probs_users_embeddings = (users_matrics[favorite_user_id - 1]).reshape([200, -1])
    probs_similarity = np.dot(users_matrics,probs_users_embeddings)
    sim = (probs_similarity)
    #     results = (-sim[0]).argsort()[0:top_k]
    #     print(results)
    #     print(sim.shape)
    #     print(np.argmax(sim, 1))
    p = np.argmax(sim, 1)
    print("喜欢看这个电影的人还喜欢看：")

    results = set()
    while len(results) != top_k//2:
        c = p[random.randrange(top_k)]
        results.add(c)
    for val in (results):
        print(val)
        print(movies_orig[val])

    return results

# recommend_other_favorite_movie(1193)




