import numpy as np
import pandas as pd
import pickle
from math import *
from numpy import *
from scipy.stats import norm

# load data and preprocess
def preprocess():
    # load data
    users = pd.read_csv('data/user.txt')
    movies = pd.read_csv('data/movie.txt')
    train = pd.read_csv('data/train.txt')
    test = pd.read_csv('data/test.txt')
    # preprocessing data
    fill_na(users)
    fill_na(movies)
    # training data
    user_train = pd.merge(users, train, how='inner', left_on='ID', right_on='user-Id')
    whole_train_data = pd.merge(user_train, movies, how='inner', left_on='movie-Id', right_on='Id')
    train_data = whole_train_data[['Gender', 'Age', 'Occupation', 'Year', 'Genre', 'rating']]
    label_pr = label_probs(train_data)
    genders = train_data['Gender'].unique()
    genres = unique(('|'.join(train_data['Genre'].unique())).split('|'))
    ratings = range(6)[1:]
    parameters = []
    parameters.append(label_pr)
    gender_probs = posterior_prob(train_data, genders, 'Gender', ratings)
    parameters.append(gender_probs)
    # genre_probs = posterior_prob(train_data, genres, 'Genre', ratings)
    # pickle.dump( genre_probs, open( 'genre_probabilities.p', 'wb' ) )
    genre_probs = pickle.load( open( 'genre_probabilities.p', 'rb' ) )
    parameters.append(genre_probs)
    age_prams = gaussian(train_data, 'Age', ratings)
    parameters.append(age_prams)
    occ_prams = gaussian(train_data, 'Occupation', ratings)
    parameters.append(occ_prams)
    year_prams = gaussian(train_data, 'Year', ratings)
    parameters.append(year_prams)
    # test data
    user_test = pd.merge(users, test, how='inner', left_on='ID', right_on='user-Id')
    whole_test_data = pd.merge(user_test, movies, how='inner', left_on='movie-Id', right_on='Id')
    test_data = whole_test_data[['Id_x', 'Gender', 'Age', 'Occupation', 'Year', 'Genre']]
    test_data = test_data.rename(index=str, columns={'Id_x': 'Id'})
    predict(test_data, parameters, genders, genres)

def predict(test_data, parameters, genders, genres):
    label(test_data.iloc[[0]], parameters, genders, genres)

def label(test_tuple, parameters, genders, genres):
    # print test_tuple
    g = test_tuple['Gender'][0]
    g_idx = where(genders == g)[0][0]
    g_probs = []
    for i in range(5):
        g_probs.append(parameters[1][2*i+g_idx])
    gr_probs = []
    gr = test_tuple['Genre'][0].split('|')
    for gi in gr:
        gr_idx = where(genres == gi)[0][0]
        gp = []
        for i in range(5):
            gp.append(parameters[2][len(genres)*i+g_idx])
        gr_probs.append(gp)
    a = test_tuple['Age'][0]
    a_probs = gaussian_prob(parameters[3], a)
    o = test_tuple['Occupation'][0]
    o_probs = gaussian_prob(parameters[4], o)
    y = test_tuple['Year'][0]
    y_probs = gaussian_prob(parameters[5], y)
    cdd = 0

def gaussian_prob(parameters, value):
    probs = []
    for p in parameters:
        probs.append(norm(p[0], p[1]).pdf(value))
    print probs
    return probs


def label_probs(train_data):
    size = train_data.shape[0]
    groups = (train_data.groupby('rating').size().reset_index(name='count')).sort('rating')
    group_probability = array(groups['count'], dtype=float)/size
    return group_probability

def gaussian(train_data, attr_name, rating):
    parameters = []
    for r in rating:
        r_data = train_data[train_data['rating'] == r]
        mu, std = norm.fit(r_data[attr_name])
        parameters.append([mu, std])
    return parameters

def posterior_prob(train_data, attr, attr_name, rating):
    probs = []
    for r in rating:
        r_data = train_data[train_data['rating'] == r]
        for a in attr:
            r_count = r_data.shape[0]
            if attr_name == 'Gender':
                count = r_data[r_data[attr_name] == a].shape[0]
            else:
                count = r_data[r_data[attr_name].str.contains(a)].shape[0]
            probs.append(float(count)/r_count)
    return probs

# assign the most common value of the attribute to missing values
def fill_na(dataframe):
    for column in dataframe:
        dataframe[column].fillna(value=dataframe[column].value_counts().idxmax(), inplace = True)

def main():   
    preprocess()

if __name__ == "__main__":
   main()