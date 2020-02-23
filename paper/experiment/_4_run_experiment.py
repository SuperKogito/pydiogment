# -*- coding: utf-8 -*-
import cmat
import time
import random
import numpy as np
import pandas as pd
from sklearn import metrics
import multiprocessing as mp
import matplotlib.pyplot as plt
from classifiers_config import classifiers
from sklearn.metrics import classification_report
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import cross_val_score, train_test_split
from dataproc import get_data, balance_dataset, pickle_save

import warnings
warnings.filterwarnings("ignore")

# global variables
scalers = {"Standard": StandardScaler(), "MinMax" : MinMaxScaler()}


def run_classification_experiment(x_train, x_test, y_train, y_test,
                                  data, X, y, classifier_name,
                                  visualziations=True, graphing=False):
    t = time.time()
    classifier = classifiers[classifier_name]
    try:
        # initialize the classifier
        clf = classifier
        clf.fit(x_train, y_train)

        # training duration
        training_duration = time.time() - t

        # score using cross-validation
        cval_scores = cross_val_score(clf, x_train, y_train, cv=5)
        test_score = clf.score(X=x_test, y=y_test)

        # print scores
        print("----------------------------------------------------------")
        print(classifier_name)
        print("----------------------------------------------------------")
        print("Cross-validation scores : ", np.round(cval_scores, 3))
        print("Testing score           : ", np.round(test_score, 3))
        print("----------------------------------------------------------")

        # predict data
        y_pred = clf.predict(x_test)
        target_names = data.emotion.unique()
        print(classification_report(y_test, y_pred, target_names=target_names))

        # compute accuraccies and confusion matrix
        accuracy = metrics.accuracy_score(y_test, y_pred)
        confusion_matrix = metrics.confusion_matrix(y_test, y_pred)

        if visualziations == True:
            # plot non-normalized confusion matrix for training set
            cmat.plot_confusion_matrix(y_train,
                                       y_pred = clf.predict(x_train),
                                       classes=y.emotion.unique(),
                                       normalize=False,
                                       title="Confusion matrix, without normalization")
            plt.show()

            # plot non-normalized confusion matrix for testing set
            cmat.plot_confusion_matrix(y_test,
                                       y_pred,
                                       classes=y.emotion.unique(),
                                       normalize=False,
                                       title="Confusion matrix, without normalization")
            plt.show()
        return clf, training_duration, accuracy, confusion_matrix

    except Exception as e:
        print("Error: faced error when testing ", classifier_name)
        print(e)


def train_model(data, model_fname, scaler_fname, scaler_type, classifier_name):
    # drop filenames
    data = data.drop(["file_name"], axis=1)
    # balance data set
    balanced_data, X, y, column_names = balance_dataset(data)

    # split data
    x_train, x_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=0.3,
                                                        random_state=random.seed(42),
                                                        shuffle=True)

    # init scaler and fit data to scaler
    if scaler_fname != "":
        scaler = scalers[scaler_type]
        scaler.fit(x_train)
        x_train = scaler.transform(x_train)
        x_test = scaler.transform(x_test)

        # export scaler to file
        pickle_save(scaler, scaler_fname)

    # run classification
    clf, t, accuracy, cmx = run_classification_experiment(x_train,
                                                          x_test,
                                                          y_train,
                                                          y_test,
                                                          data,
                                                          X,
                                                          y,
                                                          classifier_name,
                                                          visualziations=False,
                                                          graphing=False)

    print("Training's duration is", t)
    # export model to file
    pickle_save(clf, model_fname)


if __name__ == "__main__":
    available_classifiers = ['K-Nearest Neighbors (distance weights)',
                             'K-Nearest Neighbors (uniform weights)',
                             'Gaussian Process', 'Decision Tree',
                             'Random Forest', 'AdaBoost', 'Naive Bayes',
                             'Quadratic Discriminant Analysis',
                             'Linear SVM', 'MLP Classifier',
                             'Extra Trees Classifier']

    # get data
    data, _ = get_data("data/data.csv")

    # data from german  file
    X = data[data['file_name'].str.contains("DE")]

    # data from from augmented german files
    Y = X[X['file_name'].str.contains("augment") | X['file_name'].str.contains("no_silence")]
    Conv = Y[Y['file_name'].str.contains("convolv")]

    # common df
    c = pd.merge(X, Y, how='inner', on=['file_name'])

    # data from original german files
    original_data = X[(~X.file_name.isin(c.file_name))]
    original_data.to_csv("data/original_data.csv")

    for clf in available_classifiers[:]:
        try:
            # train using original data then original + augmented data
            train_model(original_data,
                        scaler_fname='min_max.scaler',
                        scaler_type="MinMax",
                        model_fname="_".join(clf.split(" ")) + "_with_min_max.model",
                        classifier_name=clf)

            # train using original + augmented data
            train_model(data,
                        scaler_fname='min_max.scaler',
                        scaler_type="MinMax",
                        model_fname="_".join(clf.split(" ")) + "_with_min_max.model",
                        classifier_name= clf)

            print("*************************************************************")
            print("*************************************************************")
            print("*************************************************************")

        except Exception as e:
            print("ERROR: ", clf)
            print(e)
