

#%%

import pandas as pd
#from pydrive.auth import GoogleAuth
#from pydrive.drive import GoogleDrive
#import pygsheets
import streamlit as st
import numpy as np
from datetime import datetime


 
#gc = pygsheets.authorize(service_file='/Users/rioz/Documents/GitHub/ZemeAnalytics/research-python-gs.json')

#open the google spreadsheet

#sh = gc.open('Py_land_data')

#select the first sheet 

#wks = sh[0]

# create dataframe

url = 'https://raw.githubusercontent.com/ri-oz/ZemeAnalytics/QA/Py_land_data%20-%20Sheet1.csv'

df_Zeme = pd.read_csv(url)

# Drop error / na rows

df_Zeme.dropna(how='any')

df_zeme_clean = df_Zeme[["Pilseta","Zemes Tips","Cena EUR","Cena m2","Platiba Daudzums","Platiba Mervieniba","Adrese","Link"]]

#%%




#df_Zeme = pd.DataFrame(wks.get_all_records())

#df_Zeme_analytics_Cena_bins = df_Zeme['Cena EUR'].value_counts(bins=20)

df_Pilseta_skaits = df_zeme_clean['Pilseta'].value_counts(ascending=True)

df_Tips_skaits = df_zeme_clean['Zemes Tips'].value_counts(ascending=True)

df_Knumurs_valid = df_Zeme['Zemes Numurs'].value_counts(ascending=True)



# %%
