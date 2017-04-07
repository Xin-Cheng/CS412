import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.multiclass import OneVsOneClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC


def main():   
    users = pd.read_csv('data/user.txt')
    movies = pd.read_csv('data/movie.txt')
    train = pd.read_csv('data/train.txt')
    test = pd.read_csv('data/test.txt')
    # preprocessing data
    le = preprocessing.LabelEncoder()
    # preprocessing movie data
    genres = movies['Genre'].unique()
    le.fit(genres)
    movies['Genre'] = le.transform(movies['Genre'])
    # preprocessing user data
    users['Occupation'].fillna(0, inplace=True)
    genders = users['Gender'].unique()
    le.fit(genders)
    users['Gender'] = le.transform(users['Gender'])
    # Training data
    user_train = pd.merge(users, train, how='inner', left_on='ID', right_on='user-Id')
    whole_train_data = pd.merge(user_train, movies, how='inner', left_on='movie-Id', right_on='Id')
    # replace missing value with 0
    whole_train_data.fillna(0, inplace=True)
    #whole_train_data.to_csv('train_data.txt')
    train_data = whole_train_data[['Gender', 'Age', 'Occupation', 'Year', 'Genre', 'rating']]
    
    # Test data
    user_test = pd.merge(users, test, how='inner', left_on='ID', right_on='user-Id')
    whole_test_data = pd.merge(user_test, movies, how='inner', left_on='movie-Id', right_on='Id')
    whole_test_data.fillna(0, inplace=True)
    #whole_test_data.to_csv('test_data.txt')
    test_data = whole_test_data[['Gender', 'Age', 'Occupation', 'Year', 'Genre']]
    test_variables = test_data.values[:,0:5]
    transaction_id = whole_test_data[['Id_x']]
    transaction = transaction_id.rename(index=str, columns={'Id_x': 'Id'})

    train_data = train_data.values
    variables = train_data[:, 0:5]
    train_ratings = train_data[:, 5]
    # decision tree classifier
    decision_tree = tree.DecisionTreeClassifier().fit(variables, train_ratings).predict(test_variables)
    transaction['rating'] = decision_tree
    transaction['rating'] = transaction['rating'].astype(int)
    result = transaction.sort(['rating'], ascending=1)
    result.to_csv('decision_tree.txt',index=False)
    # GaussianNB classifer
    nb = GaussianNB().fit(variables, train_ratings).predict(test_variables)
    transaction['rating'] = nb
    transaction['rating'] = transaction['rating'].astype(int)
    result = transaction.sort(['rating'], ascending=1)
    result.to_csv('gaussianNB.txt',index=False)
    # OneVsOneClassifier
    onevsone = OneVsOneClassifier(LinearSVC(random_state=0)).fit(variables, train_ratings).predict(test_variables)
    transaction['rating'] = onevsone
    transaction['rating'] = transaction['rating'].astype(int)
    result = transaction.sort(['rating'], ascending=1)
    result.to_csv('onevsone.txt',index=False)
    # OneVsRestClassifier
    onevsrest = OneVsRestClassifier(LinearSVC(random_state=0)).fit(variables, train_ratings).predict(test_variables)
    transaction['rating'] = onevsrest
    transaction['rating'] = transaction['rating'].astype(int)
    result = transaction.sort(['rating'], ascending=1)
    result.to_csv('onevsrest.txt',index=False)

if __name__ == "__main__":
   main()