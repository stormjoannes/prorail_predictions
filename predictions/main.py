import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import scipy.stats as st
import numpy


def read_file(file):
    dt = pd.read_csv(file, low_memory=False)
    return dt


data = read_file('../files/cleaned_data.csv')


def DecisionTreeRTrain(features, target, inpYN):
    x = features
    y = target

    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)

    decision_tree_r = DecisionTreeRegressor(max_depth=9)
    decision_tree_r.fit(x_train, y_train)

    y_pred = decision_tree_r.predict(x_test)

    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    if len(inpYN) > 0:
        betrouwbaarheid = inputFeatures(inpYN, decision_tree_r, numpy.mean(y_pred), stdv)

    return decision_tree_r, rmse, betrouwbaarheid


def inputFeatures(features, decision_tree_r, gemm, stdv):
    features = np.reshape([features], (-1, 1)).T
    inpPredict = decision_tree_r.predict(features)
    zScore = (inpPredict - gemm) / stdv

    print('Z-score', zScore)
    print('betrouwbaarheid', st.norm.cdf(zScore) * 100, ' %')


def DecisionTreeRPredict(tree, features):
    x = features

    prediction = tree.predict(x)

    return prediction


featureList = ['month', 'hour', 'stm_prioriteit', 'stm_km_tot_mld', 'stm_oorz_code']

data = data.dropna(subset=featureList)

features = data[featureList]
target = data[["stm_hersteltijd"]]

dtr, rmse = DecisionTreeRTrain(features, target, '')
