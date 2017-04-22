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
    # calculate entropy of training dataset
    entr = entropy(train_data)
    # calculate infomation gain of each feature
    feature_names = list(train_data)
    # gender_info = discrete_information(train_data, feature_names[0])
    # genre_info = combined_discrete_info(train_data, feature_names[4])
    age_split, age_info = continuous_info(train_data, feature_names[1])
    print age_split, age_info

# calculate continuous feature, 'Age', 'Occupation', and 'Year' in this project
def continuous_info(train_data, f_name):
    size = train_data.shape[0]
    features = train_data[f_name].unique()
    sorted_features = sort(features)
    split_info = zeros(len(sorted_features) - 1, dtype=float)
    split_points = zeros(len(sorted_features) - 1, dtype=float)
    # find split point
    for i in range(len(sorted_features) - 1):
        split = (sorted_features[i] + sorted_features[i + 1])/2
        split_points[i] = split
        left = train_data[train_data[f_name] <= split]
        right = train_data[train_data[f_name] > split]
        info = entropy(left)*(float(left.shape[0])/size) + entropy(right)*(float(right.shape[0])/size)
        split_info[i] = info
    min_split = argmin(split_info)
    print sorted_features
    print split_points
    return split_points[min_split], split_info[min_split]

# calculate combined discrete feature, genre in this project
def combined_discrete_info(train_data, f_name):
    size = train_data.shape[0]
    # get distinct genres
    genres_str = '|'.join(train_data['Genre'].unique())
    genres = np.unique(genres_str.split('|'))
    # calculate entropy of each distinct value
    counts = zeros(len(genres), dtype=float)
    eps = zeros(len(genres))
    for i in range(len(genres)):
        group = train_data[train_data['Genre'].str.contains(genres[i])]
        counts[i] = group.shape[0]
        eps[i] = entropy(group)
    group_probability = (counts/size)/sum(counts/size)
    info = dot(group_probability, eps)
    return info

# calculate information of discrete feature, gender in this project
def discrete_information(train_data, f_name):
    size = train_data.shape[0]
    # calculate the probability of each distinct value of this feature
    groups = train_data.groupby(f_name)
    counts = groups.size().reset_index(name='count')
    group_probability = array(counts['count'], dtype=float)/size
    # calculate entropy of each distinct value
    distinct_names = train_data[f_name].unique()
    eps = zeros(len(distinct_names))
    for i in range(len(distinct_names)):
        eps[i] = entropy(groups.get_group(distinct_names[i]))
    info = dot(group_probability, eps)
    return info

# calculate entropy
def entropy(group):
    size = group.shape[0]
    groups = group.groupby('rating').size().reset_index(name='count')
    ratings = array(groups['rating'])
    counts = array(groups['count'], dtype=float)
    probabilities = counts/size
    log_probabilities = -log2(probabilities)
    entropy = dot(probabilities, log_probabilities)
    return entropy

# assign the most common value of the attribute to missing values
def fill_na(dataframe):
    for column in dataframe:
        dataframe[column].fillna(value=dataframe[column].value_counts().idxmax(), inplace = True)

def main():   
    preprocess()

if __name__ == "__main__":
   main()