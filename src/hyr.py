# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.0
#   kernelspec:
#     display_name: ml
#     language: python
#     name: ml
# ---

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from sklearn import datasets, neighbors, metrics, tree, svm, preprocessing, model_selection, ensemble
from sklearn.model_selection import StratifiedKFold


# +
# %%time

print("loading data")
# load labels
labels = pd.read_csv('../data/Lauren/Labels.csv')
#labels.head() # to display the first 5 lines of loaded data

# load data
df = pd.read_csv('../data/Lauren/500_PBMC_3p_LT_Chromium_X_metrics_summary.csv') # takes about 5min

print("data loaded")

# +
# %%time
print("filtering data")
# filter out certain data
def gereral_data_filter(df, labels, filter_on, amount_higher_than):
    ## Filter info
    classes_count = labels.groupby(filter_on).count()
    classes_to_keep = list(classes_count[classes_count[classes_count.columns[-1]] >= amount_higher_than].index)
    keep_indices = labels[filter_on].isin(classes_to_keep)
    
    ## delete entries part of class that's too small, remove names column
    return (df[keep_indices].drop(columns=["Unnamed: 0"]), labels[keep_indices])

df, labels = gereral_data_filter(df, labels, "cluster", 10)
# -



# +
def train_linear_nn(df, labels, class_column_name): # todo: give linear classifier as argument
    # only keep the needed column
    drop_columns = filter(lambda col: col != class_column_name , labels.columns)
    labels = labels.drop(columns = drop_columns).values.ravel()
    
    # use this to split dataset in 2 parts, test and train
    skf = StratifiedKFold(n_splits=2, random_state=1337, shuffle=True)
    
    for train_index, test_index in skf.split(df, labels):
        #test_index, train_index = train_index, test_index # train on 1/5 of the data, test on 4/5ths
        # get train and test set
        X_train, X_test = df.take(train_index), df.take(test_index)
        y_train, y_test = labels[train_index], labels[test_index]
        
        # 1vRest training
        print("TRAIN:", train_index, "TEST:", test_index)
        print("Start fitting")
        lin_clf = svm.LinearSVC()
        lin_clf.fit(X_train, y_train)
        
        # predicting
        print("Start predicting")
        y_pred_lin_clf = lin_clf.predict(X_test)
        
        # metrics
        #print("Calculating metrics")
        
        print(f"F1 macro-average: {metrics.f1_score(y_test, y_pred_lin_clf, average='macro')}")
        print(f"F1 weighted-average: {metrics.f1_score(y_test, y_pred_lin_clf, average='weighted')}")
        f1 = metrics.f1_score(y_test, y_pred_lin_clf, average=None)
        print(f"accuracy: {metrics.accuracy_score(y_test, y_pred_lin_clf)}")
        
        unique_labels_df = pd.DataFrame(pd.Series(y_test).unique())
        f1_df = pd.DataFrame(f1)
        print(pd.concat([unique_labels_df, f1_df], axis=1, keys=['dcluster', 'f1_per_dcluster']))
        
        # just do 1 iteration
        return (lin_clf, f1)
    
    
#drop_columns = filter(lambda col: col != "Class" , labels.columns)
#list(drop_columns)

# -

# %%time
# as a test, train the first neural network to divide the data into Classes
(clf, all_f1) = train_linear_nn(df, labels, "Class")
all_f1


