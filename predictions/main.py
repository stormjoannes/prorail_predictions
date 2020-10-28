import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import seaborn as sns
import matplotlib.pyplot as plt
import datetime

#inlezen data
data = pd.read_csv('../files/sap_storing_data_hu_subset.csv', low_memory=False)

def dropData(selected_column, threshold):
    """
    verwijderen van de functieherstellen langer dan 6 uur.
    """
    data.drop(data.loc[data[selected_column] >= threshold].index, inplace=True)

def stringToDatetime(column):
    data[column] = pd.to_datetime(data[column])

#def linearRegression(features, target, pltTitle, xTitle, yTitle, xMin, xMax, yMin, yMax):
def linearRegression(features, target):
    x = features
    y = target

    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state = 0)

    linear_regressor = LinearRegression()
    linear_regressor.fit(x_train, y_train)

    print('coef ',linear_regressor.coef_)
    print('intercept ', linear_regressor.intercept_)

    y_pred = linear_regressor.predict(x_test)
    print(y_pred)
    print(y_test)

    print('score ', linear_regressor.score(x_test, y_test))
    print('rmse', np.sqrt(mean_squared_error(y_test, y_pred)))


def DecisionTreeR(features, target):
    x = features
    y = target

    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)

    decision_tree_r = DecisionTreeRegressor(max_depth=12)
    decision_tree_r.fit(x_train, y_train)

    y_pred = decision_tree_r.predict(x_test)
    print(y_pred)
    print(y_test)

    print('score ', r2_score(y_test, y_pred))
    print('rsme ', mean_squared_error(y_test, y_pred))


def DecisionTreeC(features, target):
    x = features
    y = target

    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)

    decision_tree_r = DecisionTreeClassifier(max_depth=10)
    decision_tree_r.fit(x_train, y_train)

    y_pred = decision_tree_r.predict(x_test)
    print(y_pred)
    print(y_test)

    print('score ', accuracy_score(y_test, y_pred))



#data preperation
dropData('stm_fh_duur', 360)
toConvertList = ['stm_sap_meld_ddt', 'stm_fh_ddt', 'stm_sap_storeind_ddt', 'stm_sap_melddatum', 'stm_aanngeb_dd',
                 'stm_progfh_in_datum', 'stm_sap_storeinddatum', 'stm_sap_storeindtijd']
for i in toConvertList:
    stringToDatetime(i)

#linearRegression
data['stm_oorz_code'] = data['stm_oorz_code'].replace(np.nan, 0)
data['month'] = pd.DatetimeIndex(data['stm_sap_meld_ddt']).month
data['hour'] = pd.DatetimeIndex(data['stm_sap_meld_ddt']).hour

# sns.pairplot(data[['month', 'stm_geo_mld', 'stm_prioriteit', 'stm_oorz_code']])
# print(data[['month', 'stm_geo_mld', 'stm_prioriteit', 'stm_oorz_code']].corr())
# plt.show()

# features = data[['month', 'stm_prioriteit', 'stm_oorz_code']]
features = data[['month', 'hour', 'stm_prioriteit', 'stm_km_tot_mld', 'stm_km_van_mld', 'stm_oorz_code']]
target = data[["stm_fh_duur"]]
# linearRegression(features, target)

DecisionTreeC(features, target)



