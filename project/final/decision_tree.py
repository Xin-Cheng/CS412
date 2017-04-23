import numpy as np
import pandas as pd
from math import *
from numpy import *

class Decision_Tree:
    def __init__(self, name, condition, is_label):
        self.name = name    # name of each tree node
        self.condition = condition
        if not is_label:
            if not condition:
                num_of_children = 1
            else:
                num_of_children = 2 if isinstance(condition, int) or isinstance(condition, float) else len(condition)
            self.children = [None]*num_of_children
    
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
    root = Decision_Tree('root', None, False)
    build_decision_tree(train_data, root.children[0])
    # test data
    user_test = pd.merge(users, test, how='inner', left_on='ID', right_on='user-Id')
    whole_test_data = pd.merge(user_test, movies, how='inner', left_on='movie-Id', right_on='Id')
    test_data = whole_test_data[['Gender', 'Age', 'Occupation', 'Year', 'Genre']]

# build decision tree
def build_decision_tree(train_data, tree_root):
    print train_data
    size = train_data.groupby('rating').size().shape[0]
    print size
    if size == 0:
        return Decision_Tree('Label', 0, True)
    elif size == 1:
        return Decision_Tree('Label', train_data['rating'][0], True)
    # find split feature
    # calculate infomation of each feature
    feature_names = list(train_data)
    information = zeros(len(feature_names) - 1)
    information_split = zeros([len(feature_names) - 1, 2])
    gender_info = discrete_information(train_data, feature_names[0])
    genre_info = combined_discrete_info(train_data, feature_names[4])
    information[0] = gender_info
    information[4] = genre_info
    for i in range(1, len(feature_names) - 2):
        info, split = continuous_info(train_data, feature_names[i])
        information_split[i, :] = [info, split]
        information[i] = info
    # choose the feature with lowest infomation as current tree node
    node_name = feature_names[argmin(information)]
    data_list = []
    if node_name == 'Gender':
        condition = ['M', 'F']
        gender_group = train_data.groupby('Gender')
        data_list.extend((groups.get_group('M'), groups.get_group('F')))
    elif node_name == 'Genre':
        condition = unique(('|'.join(train_data[node_name].unique())).split('|'))
        for c in condition:
            data_list.append(train_data[train_data['Genre'].str.contains(c)])
    else:
        condition = information_split[argmin(information)][1]
        data_list.extend((train_data[train_data[node_name] <= condition], train_data[train_data[node_name] > condition]))
    tree_root = Decision_Tree(node_name, condition, False)
    for i in range(len(data_list)):
        new_data = data_list[i].drop(node_name, axis=1)
        build_decision_tree(new_data, tree_root.children[i])

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
    return split_info[min_split], split_points[min_split]

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