import pandas as pd
import numpy as np


def read_file(file):
    dt = pd.read_csv(file, low_memory=False)
    return dt


data = read_file('../files/sap_storing_data_hu_project.csv')


def select_columns(columns, data):
    dt = data[columns]

    return dt


data = select_columns(["#stm_sap_meldnr", "stm_sap_meld_ddt", "stm_geo_mld", "stm_prioriteit", "stm_aanngeb_ddt"
, "stm_oh_pg_gst", "stm_geo_mld", "stm_km_van_gst", "stm_km_tot_gst", "stm_km_tot_mld", "stm_oorz_groep", "stm_oorz_code"
, "stm_fh_ddt", "stm_fh_status", "stm_sap_storeind_ddt", "stm_tao_indicator", "stm_tao_indicator_vorige", "stm_tao_soort_mutatie"
, "stm_tao_telling_mutatie", "stm_tao_beinvloedbaar_indicator", "stm_sap_melddatum", "stm_sap_meldtijd", "stm_techn_mld"
, "stm_techn_gst", "stm_aanngeb_dd", "stm_aanngeb_tijd", "stm_aanntpl_dd", "stm_aanntpl_tijd", "stm_progfh_in_datum"
, "stm_progfh_in_tijd", "stm_progfh_in_invoer_dat", "stm_progfh_in_invoer_tijd", "stm_progfh_in_duur", "stm_progfh_gw_tijd"
, "stm_fh_dd", "stm_fh_tijd", "stm_fh_duur", "stm_reactie_duur", "stm_sap_storeinddatum", "stm_sap_storeindtijd"
], data)


data['stm_aanntpl_tijd_merge'] = data['stm_aanntpl_dd'] + ' ' + data['stm_aanntpl_tijd']


def stringToDatetime(column):
    data[column] = pd.to_datetime(data[column])


toConvertList = ['stm_aanntpl_tijd_merge', 'stm_fh_ddt', 'stm_sap_meld_ddt',
                 'stm_sap_storeind_ddt', 'stm_sap_melddatum', 'stm_aanngeb_dd', 'stm_sap_storeinddatum']

for i in toConvertList:
    stringToDatetime(i)

data['stm_hersteltijd'] = (data['stm_fh_ddt'] - data['stm_aanntpl_tijd_merge']).astype('timedelta64[m]')

data['stm_oorz_code'] = data['stm_oorz_code'].replace(np.nan, 0)
data['month'] = pd.DatetimeIndex(data['stm_sap_meld_ddt']).month
data['hour'] = pd.DatetimeIndex(data['stm_sap_meld_ddt']).hour


def dropData(selected_column, greaterSmaller, threshold):
    """
    verwijderen van de functieherstellen langer dan 6 uur.
    """
    if greaterSmaller == '>':
        data.drop(data.loc[data[selected_column] > threshold].index, inplace=True)
    elif greaterSmaller == '<':
        data.drop(data.loc[data[selected_column] < threshold].index, inplace=True)


data = data.drop_duplicates(subset=['#stm_sap_meldnr'])
data = data[data['stm_hersteltijd'].notna()]
dropData("stm_fh_duur", '<', 3)
dropData("stm_hersteltijd", '<', 0)
dropData("stm_hersteltijd", '>', 360)


data.to_csv('cleaned_data.csv', index=False)
