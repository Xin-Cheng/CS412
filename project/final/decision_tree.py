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
    print probabilities
    print log_probabilities
    print entropy, sum(probabilities)
    cdd = 1

# assign the most common value of the attribute to missing values
def fill_na(dataframe):
    for column in dataframe:
        dataframe[column].fillna(value=dataframe[column].value_counts().idxmax(), inplace = True)

def main():   
    preprocess()

if __name__ == "__main__":
   main()