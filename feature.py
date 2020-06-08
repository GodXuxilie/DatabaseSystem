import torch.nn as nn
import torch
from torch.autograd import Variable
import pickle
import numpy as np
from torch.utils.data import SubsetRandomSampler, TensorDataset
import os
from model import *
import torch.optim as optim
import datetime

seed = 1
torch.manual_seed(seed)
np.random.seed(seed)
torch.cuda.manual_seed_all(seed)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

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

def movie_feature():
    MF = []
    model.eval()
    for item in movies.values:
        categories = np.zeros([1, 18])
        categories[0] = item.take(2)
        titles = np.zeros([1, sentences_size])
        titles[0] = item.take(1)

        movie_id = np.reshape(item.take(0), [1]),
        movie_categories = categories
        movie_titles = titles

        movie_id,movie_categories,movie_titles = torch.LongTensor(movie_id).reshape(1),torch.LongTensor(movie_categories),torch.LongTensor(movie_titles)
        uid = torch.LongTensor([1])
        user_gender = torch.LongTensor([1])
        user_age = torch.LongTensor([1])
        user_job = torch.LongTensor([1])
        user_feature, movie_feature, rating = model(uid, user_gender, user_age, user_job, movie_id, movie_categories,
                                                    movie_titles)
        # print(movie_feature.shape)

        MF.append(movie_feature.detach().numpy())
    pickle.dump((np.array(MF).reshape(-1, 200)), open('movie_matrics.p', 'wb'))

# movie_feature()
movie_matrics = pickle.load(open('movie_matrics.p', mode='rb'))
# print(movie_matrics.size,movies.size)

def user_feature():
    UF = []
    model.eval()
    for item in users.values:

        movie_id,movie_categories,movie_titles = torch.LongTensor([1]).reshape(1),torch.ones((1,18)).long(),torch.ones((1,15)).long()
        uid = np.reshape(item.take(0), [1])
        user_gender = np.reshape(item.take(1), [1])
        user_age = np.reshape(item.take(2), [1])
        user_job = np.reshape(item.take(3), [1])
        uid, user_gender, user_age, user_job, = torch.LongTensor(uid), torch.LongTensor(user_gender) \
            , torch.LongTensor(user_age), torch.LongTensor(user_job)

        user_feature, movie_feature, rating = model(uid, user_gender, user_age, user_job, movie_id, movie_categories,
                                                    movie_titles)

        UF.append(user_feature.detach().numpy())
    pickle.dump((np.array(UF).reshape(-1, 200)), open('user_matrics.p', 'wb'))

# user_feature()
user_matrics = pickle.load(open('user_matrics.p', mode='rb'))
# print(user_matrics.size,users.size)