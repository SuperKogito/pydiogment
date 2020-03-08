# -*- coding: utf-8 -*-
import pickle
import pandas as pd


def pickle_save(object_to_save, fname):
    """
    Save data to file using pickle,
    """
    pickle.dump(object_to_save, open(fname, 'wb'))


def pickle_load(fname):
    """
    Load data from file using pickle.
    """
    # load the model
    loaded_object = pickle.load(open(fname, 'rb'))
    return loaded_object


def get_data(file_path, drop_columns=True, drop_nans=True):
    # load data
    data = pd.read_csv(file_path)

    # define column names
    column_names = list(data.columns)

    if drop_columns:
        # drop columns with nans
        for c in column_names:
            if not(any(x in c for x in ["file_name", "mfcc", "duration", "emotion"])):
                del data[c]

    # drop erroneous rows
    if drop_nans:
        data = data.dropna()

    # round data
    data = data.round(3)
    data = data.iloc[:, :]

    # re-define column names
    column_names = list(data.columns)
    return data, list(data.columns)


def balance_dataset(data):
    # define column names
    column_names = list(data.columns)

    # assert equal number o samples per class
    samples_pro_emotion = {e: len(data[data.emotion == e]) for e in data.emotion.unique()}
    balanced_data = pd.concat([data[data.emotion == e].sample(min(samples_pro_emotion.values()))
                               for e in data.emotion.unique()],
                               axis=0,
                               keys=list(data.columns))

    # split data
    X = balanced_data.iloc[:, :-1]
    y = balanced_data.iloc[:, -1:].astype('category')
    # print("%25s : %s" % ("Data with balanced sets", str(balanced_data.shape)))
    return balanced_data, X, y, column_names
