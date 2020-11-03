import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
import datetime
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn import tree
import graphviz
import random

#inlezen data
data = pd.read_csv('../files/sap_storing_data_hu_project.csv', low_memory=False)

data['stm_aanntpl_tijd_merge'] = data['stm_aanntpl_dd'] + ' ' + data['stm_aanntpl_tijd']

data['stm_aanntpl_tijd_merge'] = pd.to_datetime(data['stm_aanntpl_tijd_merge'])
data['stm_fh_ddt'] = pd.to_datetime(data['stm_fh_ddt'])
data['stm_sap_meld_ddt'] = pd.to_datetime(data['stm_sap_meld_ddt'])
data['stm_sap_storeind_ddt'] = pd.to_datetime(data['stm_sap_storeind_ddt'])
data['stm_sap_melddatum'] = pd.to_datetime(data['stm_sap_melddatum'])
data['stm_aanngeb_dd'] = pd.to_datetime(data['stm_aanngeb_dd'])

data['stm_sap_storeinddatum'] = pd.to_datetime(data['stm_sap_storeinddatum'])

data['stm_hersteltijd'] = (data['stm_fh_ddt'] - data['stm_aanntpl_tijd_merge']).astype('timedelta64[m]')

data = data.drop_duplicates(subset=['#stm_sap_meldnr'])
data = data[data['stm_hersteltijd'].notna()]
data.drop(data.loc[data["stm_fh_duur"] < 3].index, inplace=True)
data.drop(data.loc[data["stm_hersteltijd"] < 0].index, inplace=True)
data.drop(data.loc[data['stm_hersteltijd'] >= 360.0].index, inplace=True)


def dropData(selected_column, threshold):
    """
    verwijderen van de functieherstellen langer dan 6 uur.
    """
    data.drop(data.loc[data[selected_column] >= threshold].index, inplace=True)


dropData('stm_hersteltijd', 360)


def stringToDatetime(column):
    data[column] = pd.to_datetime(data[column])


def DecisionTreeR(features, target):
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


data['stm_oorz_code'] = data['stm_oorz_code'].replace(np.nan, 0)
data['month'] = pd.DatetimeIndex(data['stm_sap_meld_ddt']).month
data['hour'] = pd.DatetimeIndex(data['stm_sap_meld_ddt']).hour

featureList = ['month', 'hour', 'stm_prioriteit', 'stm_km_tot_mld', 'stm_oorz_code']

data = data.dropna(subset=featureList)

features = data[featureList]
target = data[["stm_hersteltijd"]]

DecisionTreeR(features, target)
