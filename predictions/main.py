import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

#inlezen data
data = pd.read_csv('../files/sap_storing_data_hu_subset.csv', low_memory=False)

def dropData(selected_column, threshold):
    """
    verwijderen van de functieherstellen langer dan 6 uur.
    """
    data.drop(data.loc[data[selected_column] >= threshold].index, inplace=True)

def stringToDatetime(column):
    data[column] = pd.to_datetime(data[column])


def linearRegression():
    x = data[['stm_sap_meld_ddt', 'stm_geo_mld', 'stm_prioriteit', 'stm_oorz_code']]
    y = data[["stm_fh_duur"]]

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


#data preperation
dropData('stm_fh_duur', 360)
toConvertList = ['stm_sap_meld_ddt', 'stm_fh_ddt', 'stm_sap_storeind_ddt', 'stm_sap_melddatum', 'stm_aanngeb_dd',
                 'stm_progfh_in_datum', 'stm_sap_storeinddatum', 'stm_sap_storeindtijd']
for i in toConvertList:
    stringToDatetime(i)

linearRegression()