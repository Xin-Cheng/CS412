import numpy as np
import pandas as pd
from math import *
from numpy import *

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
    # build decision tree
    build_decision_tree(train_data)
    # test data
    user_test = pd.merge(users, test, how='inner', left_on='ID', right_on='user-Id')
    whole_test_data = pd.merge(user_test, movies, how='inner', left_on='movie-Id', right_on='Id')
    test_data = whole_test_data[['Gender', 'Age', 'Occupation', 'Year', 'Genre']]

# build decision tree
def build_decision_tree(train_data):
    # get distinct genres
    # genres_str = '|'.join(movies['Genre'].unique())
    # genres = np.unique(genres_str.split('|'))
    # calculate entropy of training dataset
    size = train_data.shape[0]
    groups = train_data.groupby('rating').size().reset_index(name='count')
    ratings = array(groups['rating'])
    counts = array(groups['count'], dtype=float)
    probabilities = counts/size
    log_probabilities = -log2(probabilities)
    entropy = dot(probabilities, log_probabilities)
    # calculate infomation gain of each feature
    feature_names = list(train_data)
    information(train_data, feature_names[0])

def information(train_data, f_name):
    size = train_data.shape[0]
    # calculate the probability of each distinct value of this feature
    groups = train_data.groupby(f_name).size().reset_index(name='count')
    group_probability = array(groups['count'], dtype=float)/size
    # calculate entropy of each distinct value
    distinct_names = train_data[f_name].unique()
    male = train_data.groupby(f_name).get_group('M')
    print groups
    print distinct_names
    print group_probability
    cdd = 0


# assign the most common value of the attribute to missing values
def fill_na(dataframe):
    for column in dataframe:
        dataframe[column].fillna(value=dataframe[column].value_counts().idxmax(), inplace = True)

def main():   
    preprocess()

if __name__ == "__main__":
   main()