import numpy as np
from sklearn import svm
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import style
style.use("ggplot")
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import GaussianNB

import pickle


clf = svm.SVC(kernel="linear", C=1.0, random_state=0)

def Build_Data_Set(features = ["r_1", "r_2", "r_3", "r_not", "siz", "is_num", "in_kwd", "only_num"]):
    data_df = pd.read_csv("first_iter.csv")
    # print(data_df.groupby("r_1")["query"].count())
    # print(data_df.groupby("r_2")["query"].count())
    # print(data_df.groupby("r_3")["query"].count())
    # print(data_df.groupby("r_not")["query"].count())
    # print(data_df.groupby("siz")["query"].count())
    # print(data_df.groupby("in_kwd")["query"].count())
    # print(data_df.groupby("is_num")["query"].count())
    # print(data_df.groupby("only_num")["query"].count())
    # print(data_df.groupby("y_n")["query"].count())
    msk = np.random.rand(len(data_df)) < 0.75
    train_df = data_df[msk]
    test_df = data_df[~msk]
    # data_df = data_df[]
    X = np.array(train_df[features].values)
    y = (train_df["y_n"].values.tolist())
    tst_X = np.array(train_df[features].values)
    tst_y = (train_df["y_n"].values.tolist())
    return X,y, tst_X, tst_y


def Analysis():
    X, y, tst_x, tst_y = Build_Data_Set()
    clf.fit(X, y)
    
    # save the model to disk
    filename = 'finalized_model_SVM.sav'
    pickle.dump(clf, open(filename, 'wb'))
    
    return tst_x, tst_y

def Predictor(tst_x, tst_y):
    # features = ["r_1", "r_2", "r_3", "r_not", "siz", "is_num", "in_kwd", "only_num"]
    # data_df = pd.read_csv("first_iter.csv")
    # data_df = data_df[:100]
    # print(tst_x[0:10])
    # X_test = tst_X
    # X_test = np.array(data_df[features].values)
    predicted = clf.predict(tst_x)
    # actual = (data_df["y_n"].values.tolist())[:100]
    # actual = tst_y["y_n"].values.tolist()
    print('Confusion Matrix:\n', confusion_matrix(tst_y, predicted))
    print('-----', accuracy_score(tst_y, predicted))

tst_x, tst_y = Analysis()
Predictor(tst_x, tst_y)


clf_GaussNB = GaussianNB()

def Build_Data_Set_GaussNB(features = ["r_1", "r_2", "r_3", "r_not", "siz", "is_num", "in_kwd", "only_num"]):
    data_df = pd.read_csv("first_iter.csv")
    # print(data_df.groupby("r_1")["query"].count())
    # print(data_df.groupby("r_2")["query"].count())
    # print(data_df.groupby("r_3")["query"].count())
    # print(data_df.groupby("r_not")["query"].count())
    # print(data_df.groupby("siz")["query"].count())
    # print(data_df.groupby("in_kwd")["query"].count())
    # print(data_df.groupby("is_num")["query"].count())
    # print(data_df.groupby("only_num")["query"].count())
    # print(data_df.groupby("y_n")["query"].count())
    msk = np.random.rand(len(data_df)) < 0.75
    train_df = data_df[msk]
    test_df = data_df[~msk]
    # data_df = data_df[]
    X = np.array(train_df[features].values)
    y = (train_df["y_n"].values.tolist())
    tst_X = np.array(train_df[features].values)
    tst_y = (train_df["y_n"].values.tolist())
    return X,y, tst_X, tst_y


def Analysis_GaussNB():
    X, y, tst_x, tst_y = Build_Data_Set_GaussNB()
    clf_GaussNB.fit(X, y)
    
    # save the model to disk
    filename = 'finalized_model_GaussNB.sav'
    pickle.dump(clf_GaussNB, open(filename, 'wb'))
    
    return tst_x, tst_y

def Predictor_GaussNB(tst_x, tst_y):
    # features = ["r_1", "r_2", "r_3", "r_not", "siz", "is_num", "in_kwd", "only_num"]
    # data_df = pd.read_csv("first_iter.csv")
    # data_df = data_df[:100]
    # print(tst_x[0:10])
    # X_test = tst_X
    # X_test = np.array(data_df[features].values)
    predicted = clf_GaussNB.predict(tst_x)
    # actual = (data_df["y_n"].values.tolist())[:100]
    # actual = tst_y["y_n"].values.tolist()
    print('Confusion Matrix GNB:\n', confusion_matrix(tst_y, predicted))
    print('-----', accuracy_score(tst_y, predicted))

tst_x, tst_y = Analysis_GaussNB()
Predictor_GaussNB(tst_x, tst_y)

