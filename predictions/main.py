import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import scipy.stats as st
import statistics as stt
import numpy


def read_file(file):
    dt = pd.read_csv(file, low_memory=False)
    return dt


data = read_file('../files/cleaned_data.csv')


def DecisionTreeRTrain(features, target):
    x = features
    y = target

    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)

    decision_tree_r = DecisionTreeRegressor(max_depth=9)
    decision_tree_r.fit(x_train, y_train)

    y_pred = decision_tree_r.predict(x_test)

    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    stdv = stt.stdev(y_pred)
    gemm = numpy.mean(y_pred)

    return decision_tree_r, rmse, stdv, gemm


def inputFeatures(features, decision_tree_r, stdv, gemm):
    features = np.reshape([features], (-1, 1)).T
    inpPredict = decision_tree_r.predict(features)
    zScore = (inpPredict - gemm) / stdv

    trust = st.norm.cdf(zScore) * 100

    return trust


def DecisionTreeRPredict(tree, features, stdv, gemm):
    x = features

    prediction = tree.predict(x)

    trust = inputFeatures(features, tree, stdv, gemm)

    return prediction, trust


featureList = ['month', 'hour', 'stm_prioriteit', 'stm_km_tot_mld', 'stm_oorz_code']

data = data.dropna(subset=featureList)

features = data[featureList]
target = data[["stm_hersteltijd"]]

dtr, rmse, stdv, gemm = DecisionTreeRTrain(features, target)
