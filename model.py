import torch.nn as nn
import torch
from torch.autograd import Variable


class Movie_Recommendation_Model(nn.Module):
    def __init__(self, uid_max, gender_max, age_max, job_max, movie_id_max, movie_categories_max, movie_title_max):
        super(Movie_Recommendation_Model, self).__init__()
        self.uid_max = uid_max
        self.gender_max = gender_max
        self.age_max = age_max
        self.job_max = job_max
        self.movie_id_max = movie_id_max
        self.movie_categories_max = movie_categories_max
        self.movie_title_max = movie_title_max

        self.uid_embed_layer = nn.Embedding(num_embeddings=uid_max,embedding_dim=32)
        self.gender_embed_layer = nn.Embedding(num_embeddings=gender_max,embedding_dim=16)
        self.age_embed_layer = nn.Embedding(num_embeddings=age_max,embedding_dim=16)
        self.job_embed_layer = nn.Embedding(num_embeddings=job_max,embedding_dim=16)

        self.uid_fc = nn.Linear(32,32)
        self.gender_fc = nn.Linear(16,32)
        self.age_fc = nn.Linear(16,32)
        self.job_fc = nn.Linear(16,32)

        self.relu_active = nn.ReLU()

        self.user_feature = nn.Linear(128,200)

        self.movie_id_embed_layer = nn.Embedding(num_embeddings=movie_id_max,embedding_dim=32)
        self.movie_categories_embed_layer = nn.Embedding(num_embeddings=movie_categories_max,embedding_dim=32)

        self.movie_id_fc = nn.Linear(32,32)
        self.movie_categories_fc = nn.Linear(32,32)

        self.movie_title_embed_layer = nn.Embedding(num_embeddings=movie_title_max,embedding_dim=32)
        self.movie_title_conv = nn.Conv2d(1, 8, 3)
        self.movie_title_pool = nn.MaxPool2d(2,2)
        self.movie_title_fc = nn.Linear(8*6*15,32)

        self.movie_feature = nn.Linear(96,200)

        self.rate_fc1 = nn.Linear(400,128)
        self.rate_fc2 = nn.Linear(128,1)

        # self.rate = nn.Linear(400,1)
        self.dropout = nn.Dropout(0.5)

    def mean(self,x):
        x_var = []
        for i in range(len(x)):
            tmp = torch.mean(x[i], dim=0, keepdim=True).squeeze().reshape(-1,32)
            if len(x_var) == 0:
                x_var = tmp
            else:
                x_var = torch.cat((x_var,tmp))
        return x_var

    def forward(self,uid, user_gender, user_age, user_job, movie_id, movie_categories, movie_titles):
        dim0 = len(uid)
        uid = self.uid_embed_layer(uid)
        uid = self.uid_fc(uid)
        user_gender = self.gender_embed_layer(user_gender)
        user_gender = self.gender_fc(user_gender)
        user_age = self.age_embed_layer(user_age)
        user_age = self.age_fc(user_age)
        user_job = self.job_embed_layer(user_job)
        user_job = self.job_fc(user_job)

        # print(uid.shape,user_gender.shape,user_age.shape,user_job.shape)
        user = torch.cat((uid,user_gender,user_age,user_job),dim=1)
        # print(user.shape)
        user = self.user_feature(user)

        movie_id = self.movie_id_embed_layer(movie_id)
        movie_id = self.movie_id_fc(movie_id)
        movie_categories = self.movie_categories_embed_layer(movie_categories)
        # print(movie_categories.shape)
        movie_categories = self.mean(movie_categories)
        # print(movie_categories.shape)
        movie_categories = self.movie_categories_fc(movie_categories)
        movie_titles = self.movie_title_embed_layer(movie_titles)
        movie_titles = movie_titles.reshape(dim0,1,15,32)
        # print(movie_titles.shape)
        movie_titles = self.movie_title_conv(movie_titles)
        # print(movie_titles.shape)
        movie_titles = self.movie_title_pool(movie_titles)
        # print(movie_titles.shape)
        movie_titles = self.dropout(movie_titles)
        movie_titles = movie_titles.reshape(dim0,-1)
        movie_titles = self.movie_title_fc(movie_titles)

        movie = torch.cat((movie_id,movie_categories,movie_titles),dim=1)
        movie = self.movie_feature(movie)
        # print(user.shape,movie.shape)
        user_movie_feature = torch.cat((user,movie),dim=1)
        rate = self.rate_fc1(user_movie_feature)
        rate = self.relu_active(rate)
        rate = self.rate_fc2(rate)

        return user,movie,rate



def MR_Model(uid_max, gender_max, age_max, job_max, movie_id_max, movie_categories_max, movie_title_max):
    return Movie_Recommendation_Model(uid_max, gender_max, age_max, job_max, movie_id_max, movie_categories_max, movie_title_max)
