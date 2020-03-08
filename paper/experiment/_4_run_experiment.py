# -*- coding: utf-8 -*-
import os
import time
import warnings
import numpy as np
import pandas as pd
from utils import cmat
from sklearn import metrics
import matplotlib.pyplot as plt
from utils.classifiers_config import classifiers
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from utils.dataproc import get_data, balance_dataset, pickle_save
from sklearn.model_selection import cross_val_score, train_test_split

warnings.filterwarnings("ignore")

# global variables
scalers = {"Standard": StandardScaler(), "MinMax" : MinMaxScaler()}


def train_model(data, model_fname, scale, classifier_name, visualizations=False):
    """
    Train ML model.
    """
    # drop filenames
    data = data.drop(["file_name"], axis=1)
    # balance data set
    balanced_data, X, y, column_names = balance_dataset(data)

    # split data
    x_train, x_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=0.3,
                                                        random_state=22,
                                                        shuffle=True)

    # init scaler and fit data to scaler
    if scale:
        scaler = MinMaxScaler()
        scaler.fit(x_train)
        x_train = scaler.transform(x_train)
        x_test = scaler.transform(x_test)

    # run classification
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

        if visualizations:
            # plot non-normalized confusion matrix for testing set
            cmat.plot_confusion_matrix(y_test,
                                       y_pred,
                                       classes=y.emotion.unique(),
                                       normalize=False,
                                       title="Confusion matrix, without normalization")
            plt.show()

    except Exception as e:
        print("Error: faced error when testing ", classifier_name)
        print(e)
        return

    print("Training's duration is", np.round(time.time() - t, 3))
    # export model to file
    pickle_save(clf, "models/" + model_fname)


if __name__ == "__main__":
    available_classifiers = ['K-Nearest Neighbors (distance weights)',
                             'K-Nearest Neighbors (uniform weights)',
                             'Gaussian Process', 'Decision Tree',
                             'Random Forest', 'AdaBoost', 'Naive Bayes',
                             'Quadratic Discriminant Analysis',
                             'Linear SVM', 'MLP Classifier',
                             'Extra Trees Classifier']

    # get data from original and augmented files
    original_data  = get_data("data/features.csv")[0]
    augmented_data = get_data("data/augmented_features.csv")[0]
    all_data       = pd.concat([original_data, augmented_data])

    # make dir
    if not (os.path.isdir("models")): os.mkdir("models")

    # experiment
    for clf in available_classifiers[:]:
        try:
            print("----------------------------------------------------------")
            print("******************* NO AUGMENTATION **********************")
            # train using original data then original + augmented data
            train_model(original_data,
                        model_fname="_".join(clf.split(" ")) + "_with_min_max.model",
                        scale=False,
                        classifier_name=clf,
                        visualizations=False)

            print("----------------------------------------------------------")
            print("******************* WITH AUGMENTATION ********************")
            # train using original + augmented data
            train_model(all_data,
                        model_fname="_".join(clf.split(" ")) + "_with_min_max.model",
                        scale=False,
                        classifier_name=clf,
                        visualizations=False)

        except Exception as e:
            print("ERROR: ", clf)
            print(e)
