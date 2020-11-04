import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split

#inlezen data


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
    print(y_pred)
    print(y_test)

    print('score ', r2_score(y_test, y_pred))
    print('rmse ', np.sqrt(mean_squared_error(y_test, y_pred)))

    return decision_tree_r


def DecisionTreeRPredict(tree, features):
    x = features

    prediction = tree.predict(x)

    print(prediction)


featureList = ['month', 'hour', 'stm_prioriteit', 'stm_km_tot_mld', 'stm_oorz_code']

data = data.dropna(subset=featureList)

features = data[featureList]
target = data[["stm_hersteltijd"]]

dtr = DecisionTreeRTrain(features, target)
