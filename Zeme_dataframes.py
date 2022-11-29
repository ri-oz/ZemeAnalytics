

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



df_tips_mean = df_zeme_clean.groupby(['Zemes Tips']).mean()
df_tips_max = df_zeme_clean.groupby(['Zemes Tips']).max()
df_tips_min = df_zeme_clean.groupby(['Zemes Tips']).min()


df_tips_mean = df_zeme_clean.groupby(['Zemes Tips']).mean()
df_tips_mean = df_tips_mean.add_prefix('Videja')

df_tips_max = df_zeme_clean.groupby(['Zemes Tips']).max()
df_tips_max = df_tips_max.drop(columns=['Pilseta', 'Platiba Mervieniba','Adrese','Link'])
df_tips_max = df_tips_max.add_prefix('Lielaka')

df_tips_min = df_zeme_clean.groupby(['Zemes Tips']).min()
df_tips_min = df_tips_min.drop(columns=['Pilseta', 'Platiba Mervieniba','Adrese','Link'])
df_tips_min = df_tips_min.add_prefix('Mazaka')

df_tips = df_tips_mean.merge(df_tips_max, left_on='Zemes Tips', right_on='Zemes Tips')
df_tips = df_tips.merge(df_tips_min,left_on='Zemes Tips', right_on='Zemes Tips')

del [[df_tips_max,df_tips_min,df_tips_mean]]


df_pilseta_mean = df_zeme_clean.groupby(['Pilseta']).mean()
df_pilseta_mean = df_pilseta_mean.add_prefix('Videja')

df_pilseta_max = df_zeme_clean.groupby(['Pilseta']).max()
df_pilseta_max = df_pilseta_max.drop(columns=['Zemes Tips', 'Platiba Mervieniba','Adrese','Link'])
df_pilseta_max = df_pilseta_max.add_prefix('Lielaka')

df_pilseta_min = df_zeme_clean.groupby(['Pilseta']).min()
df_pilseta_min = df_pilseta_min.drop(columns=['Zemes Tips', 'Platiba Mervieniba','Adrese','Link'])
df_pilseta_min = df_pilseta_min.add_prefix('Mazaka')

df_pilseta = df_pilseta_mean.merge(df_pilseta_max, left_on='Pilseta', right_on='Pilseta')
df_pilseta = df_pilseta.merge(df_pilseta_min,left_on='Pilseta', right_on='Pilseta')

del [[df_pilseta_max,df_pilseta_min,df_pilseta_mean]]

# %%


