import pandas as pd
from sklearn import preprocessing
from sklearn import svm
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.cross_validation import cross_val_score
# from sklearn import model_selection
# from sklearn.metrics import classification_report
# from sklearn.metrics import confusion_matrix
# from sklearn.metrics import accuracy_score
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.naive_bayes import GaussianNB
# from sklearn.svm import SVC


def main():
    users = pd.read_csv('data/user.txt')
    movies = pd.read_csv('data/movie.txt')
    train = pd.read_csv('data/train.txt')
    test = pd.read_csv('data/test.txt')
    # print test
    # Training data
    user_train = pd.merge(users, train, how='inner', left_on='ID', right_on='user-Id')
    whole_train_data = pd.merge(user_train, movies, how='inner', left_on='movie-Id', right_on='Id')
    train_data = whole_train_data[['Gender', 'Age', 'Occupation', 'Year', 'Genre', 'rating']]
    le = preprocessing.LabelEncoder().fit(train_data[['Genre']])
    train_data['Genre'] = le.transform(train_data[['Genre']])
    le = preprocessing.LabelEncoder().fit(train_data[['Gender']])
    train_data['Gender'] = le.transform(train_data[['Gender']])
    print train_data
    train_data.fillna(train_data.mean(), inplace=True)
    print train_data
     
    train_data = train_data.values
    variables = train_data[:, 0:5]
    print variables
    train_ratings = train_data[:, 5]
    print train_ratings[2]
    et = ExtraTreesClassifier()
    et_score = cross_val_score(et, variables, train_ratings).mean()
    clf = svm.SVC()
    clf.fit(variables, train_ratings)
    # print train_data.columns
    # dtc = model_selection.cross_val_score(DecisionTreeClassifier(), variables, train_ratings, scoring=scoring)
    cdd = 1
    print 'finish'

if __name__ == "__main__":
   main()