import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

#inlezen data
data = pd.read_csv('../files/sap_storing_data_hu_subset.csv', low_memory=False)

#verwijderen van de functieherstellen langer dan 6 uur
data.drop(data.loc[data['stm_fh_duur'] >= 360].index, inplace=True)
highNumbers = data["stm_fh_duur"][data["stm_fh_duur"] == 0] #alles boven de 6 uur duur weggooien.
print(highNumbers)