import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn import svm


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
    whole_train_data.to_csv('train_data.txt')
    train_data = whole_train_data[['Gender', 'Age', 'Occupation', 'Year', 'Genre', 'rating']]
    
    # Test data
    user_test = pd.merge(users, test, how='inner', left_on='ID', right_on='user-Id')
    whole_test_data = pd.merge(user_test, movies, how='inner', left_on='movie-Id', right_on='Id')
    whole_test_data.fillna(0, inplace=True)
    whole_test_data.to_csv('test_data.txt')
    test_data = whole_test_data[['Gender', 'Age', 'Occupation', 'Year', 'Genre']]
    test_variables = test_data.values[:,0:5]
     
    train_data = train_data.values
    variables = train_data[:, 0:5]
    train_ratings = train_data[:, 5]

    svm_model = svm.SVC()
    svm_model.fit(variables, train_ratings)
    result = svm_model.predict(test_variables)
    svm_file = open('svm.txt', 'w')
    for item in result:
        svm_file.write("%s\n" % item)
    print result
    # print train_data.columns
    # dtc = model_selection.cross_val_score(DecisionTreeClassifier(), variables, train_ratings, scoring=scoring)

if __name__ == "__main__":
   main()