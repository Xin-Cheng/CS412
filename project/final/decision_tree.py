import numpy as np
import pandas as pd
import pickle
from math import *
from numpy import *

class Decision_Tree:
    def __init__(self, name, condition, is_label):
        self.name = name    # name of each tree node
        self.condition = condition
        self.constraint = None
        if condition is None or is_label:
            num_of_children = 1
        else:
            num_of_children = 2 if isinstance(condition, int) or isinstance(condition, float) else len(condition)
        self.children = [None]*num_of_children
    def set_constraint(self, constraint):
        self.constraint = constraint
    
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
    # root = Decision_Tree('root', None, False)
    # build_decision_tree(train_data, root)
    # pickle.dump( root, open( 'decision_tree.p', 'wb' ) )
    my_tree = pickle.load( open( 'decision_tree.p', 'rb' ) )
    # test data
    user_test = pd.merge(users, test, how='inner', left_on='ID', right_on='user-Id')
    whole_test_data = pd.merge(user_test, movies, how='inner', left_on='movie-Id', right_on='Id')
    test_data = whole_test_data[['Gender', 'Age', 'Occupation', 'Year', 'Genre']]
    predict(test_data, my_tree)

def predict(test_data, decision_tree):
    test_data['rating'] = 0
    build_queries(decision_tree)
    # exec(cdd)
    print test_data
    cdd = 0

def build_queries(decision_tree):
    queries = []
    prefix = 'test_data.loc['
    suffix = ', "rating"] ='
    node_list = []
    while node_list:
        node_stack.append(curr_node)
        if curr_node.constraint is not None:
            constraint_stack.append(curr_node.constraint)
    cxx = 1

# find split feature according to information gain
def find_split(train_data):
    size = train_data.groupby('rating').size().shape[0]
    if size == 1:
        return Decision_Tree('label', train_data['rating'].tolist()[0], True)
    # go for majority vote
    elif train_data.shape[1] == 1:
        return Decision_Tree('label', bincount(train_data['rating']).argmax(), True)
    # find split feature
    # calculate infomation of each feature
    feature_names = list(train_data)
    information = zeros(len(feature_names) - 1)
    information_split = zeros([len(feature_names) - 1, 2])
    for i in range(0, len(feature_names) - 1):
        if feature_names[i] == 'Gender':
            information[i] = discrete_information(train_data, feature_names[i])
        elif feature_names[i] == 'Genre':
            information[i] = combined_discrete_info(train_data, feature_names[i])
        else:
            info, split = continuous_info(train_data, feature_names[i])
            information_split[i, :] = [info, split]
            information[i] = info
    # choose the feature with lowest infomation as current tree node
    node_name = feature_names[argmin(information)]
    if node_name == 'Gender':
        condition = ['M', 'F']
    elif node_name == 'Genre':
        condition = unique(('|'.join(train_data[node_name].unique())).split('|'))
    else:
        condition = information_split[argmin(information)][1]
    return Decision_Tree(node_name, condition, False)
    
# build decision tree
def build_decision_tree(train_data, tree_root):
    if tree_root.condition is None:
        tree_root.children[0] = find_split(train_data)
        build_decision_tree(train_data, tree_root.children[0])
    elif tree_root.name == 'label':
        return
    else: 
        condition = tree_root.condition
        name = tree_root.name
        prev_constraint = tree_root.constraint + ' & ' if tree_root.constraint is not None else ''
        if name != 'Genre':
            left = (train_data[train_data[name] <= condition] if name != 'Gender' else train_data.groupby('Gender').get_group('M')).drop(name, axis=1)
            right = (train_data[train_data[name] > condition] if name != 'Gender' else train_data.groupby('Gender').get_group('F')).drop(name, axis=1)
            tree_root.children[0] = find_split(left)
            tree_root.children[1] = find_split(right)
            if name != 'Gender':
                tree_root.children[0].set_constraint(prev_constraint + '(test_data[\"' + name + '\"]' + '<=' + str(condition) + ')')
                tree_root.children[1].set_constraint(prev_constraint + '(test_data[\"' + name + '\"]' + '>' + str(condition) + ')')
            else:
                tree_root.children[0].set_constraint(prev_constraint + '(test_data["Gender"] == \"M\")')
                tree_root.children[1].set_constraint(prev_constraint + '(test_data["Gender"] == \"F\")')
            build_decision_tree(left, tree_root.children[0])
            build_decision_tree(right, tree_root.children[1])
        else:
            for i in range(len(condition)):
                group = (train_data[train_data['Genre'].str.contains(condition[i])]).drop(name, axis=1)
                tree_root.children[i] = find_split(group)
                tree_root.children[i].set_constraint(prev_constraint + '(test_data[\"' + name + '\"]' + '==' + '\"' + condition[i] + '\"' + ')')
                build_decision_tree(group, tree_root.children[i])

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