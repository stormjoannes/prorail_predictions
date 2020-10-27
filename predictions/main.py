import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

data = pd.read_csv('../sap_storing_data_hu_subset.csv', low_memory=False)
