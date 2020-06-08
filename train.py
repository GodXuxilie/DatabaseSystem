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

lr = 0.00005
momentum = 0.9
weight_decay = 2e-4
batch_size = 256
validation_split = .2
shuffle_dataset = True
random_seed = seed

movieid2idx = {val[0]:i for i, val in enumerate(movies.values)}

model = MR_Model(uid_max, gender_max, age_max, job_max, movie_id_max, movie_categories_max, movie_title_max)
optimizer = optim.SGD(model.parameters(), lr=lr, momentum=momentum, weight_decay=weight_decay)
criterion = nn.MSELoss(reduction="mean")

dataset_size = len(features)
indices = list(range(dataset_size))
split = int(np.floor(validation_split * dataset_size))
if shuffle_dataset :
    np.random.seed(random_seed)
    np.random.shuffle(indices)
train_indices, val_indices = indices[split:], indices[:split]

train_sampler = SubsetRandomSampler(train_indices)
valid_sampler = SubsetRandomSampler(val_indices)

trainx = []
for i in range(len(features)):
    t = []
    x = features[i]
    t.append(x[0])
    t.append(x[1])
    t.append(x[2])
    t.append(x[3])
    t.append(x[4])
    for tmp in x[5]:
        t.append(tmp)
    for tmp in x[6]:
        t.append(tmp)
    trainx.append(t)

features = torch.Tensor(trainx)
targets_values = torch.Tensor(targets_values)
# print(targets_values[1:10])
dataset = TensorDataset(features,targets_values)

train_loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size,sampler=train_sampler)
validation_loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size,sampler=valid_sampler)


def train(model,train_loader, optimizer):
    starttime = datetime.datetime.now()
    loss_sum = 0
    correct = 0
    for batch_idx, (data, target) in enumerate(train_loader):
        target = target.squeeze()
        model.train()
        optimizer.zero_grad()

        uid = data[:,0].long()
        user_gender = data[:,2].long()
        user_age = data[:,3].long()
        user_job = data[:,4].long()
        movie_id = data[:,1].long()
        movie_titles = data[:,5:20].long()
        movie_categories = data[:,20:38].long()
        # print(uid.shape,user_gender.shape,user_age.shape,user_job.shape,movie_id.shape,movie_categories.shape,movie_titles.shape)
        user_feature,movie_feature,rating = model(uid, user_gender, user_age, user_job, movie_id, movie_categories, movie_titles)
        # print(rating.shape,target.shape)
        # pred = rating.max(1, keepdim=True)[1]
        # correct += pred.eq(target.view_as(pred)).sum().item()
        loss = criterion(rating,target)
        loss_sum += loss.item()
        loss.backward()
        optimizer.step()
        if batch_idx % 100 == 0:
            print(batch_idx,loss.item())

    endtime = datetime.datetime.now()
    time = (endtime - starttime).seconds
    return time, loss_sum

def eval_testloss(model,validation_loader):
    model.eval()
    loss_sum = 0
    correct = 0
    for batch_idx, (data, target) in enumerate(validation_loader):
        target = target.squeeze()
        uid = data[:, 0].long()
        user_gender = data[:, 2].long()
        user_age = data[:, 3].long()
        user_job = data[:, 4].long()
        movie_id = data[:, 1].long()
        movie_titles = data[:, 5:20].long()
        movie_categories = data[:, 20:38].long()
        user_feature, movie_feature, rating = model(uid, user_gender, user_age, user_job, movie_id, movie_categories,movie_titles)
        # pred = rating.max(1, keepdim=True)[1]
        # correct += pred.eq(target.view_as(pred)).sum().item()
        loss = criterion(rating, target)
        loss_sum += loss.item()
    return loss_sum

epochs = 5

for epoch in range(0, epochs):
    print("====>epoch:{}".format(epoch))
    time, train_loss = train(model, train_loader, optimizer)
    valid_loss = eval_testloss(model,validation_loader)
    print('time:{}\ttrain_acc:{}\tvalid_acc:{}'.format(time,train_loss,valid_loss))
    torch.save(model.state_dict(), os.path.join(model_dir, 'lr_checkpoint.pt'))
