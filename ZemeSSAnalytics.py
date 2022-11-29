

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


#df_Zeme = pd.DataFrame(wks.get_all_records())

#df_Zeme_analytics_Cena_bins = df_Zeme['Cena EUR'].value_counts(bins=20)

df_Zeme_analytics_Pilseta_skaits = df_Zeme['Pilseta'].value_counts(ascending=True)

df_Zeme_analytics_Tips_skaits = df_Zeme['Zemes Tips'].value_counts(ascending=True)

df_Zeme_max_min_avg_cena_eur = df_Zeme.groupby('Pilseta').agg({'Cena EUR': ['mean', 'min', 'max']})
df_Zeme_max_min_avg_cena_m2 = df_Zeme.groupby('Pilseta').agg({'Cena m2': ['mean', 'min', 'max']})

df_Zeme_max_min_avg_izmers = df_Zeme.groupby('Pilseta').agg({'Platiba Daudzums': ['mean', 'min', 'max']})

#new_header1 = df_Zeme_max_min_avg_cena_eur.iloc[0] #grab the first row for the header
#df_Zeme_max_min_avg_cena_eur = df_Zeme_max_min_avg_cena_eur[1:] #take the data less the header row
#df_Zeme_max_min_avg_cena_eur.columns = new_header1

new_header2 = df_Zeme_max_min_avg_cena_m2.iloc[0] 
df_Zeme_max_min_avg_cena_m2 = df_Zeme_max_min_avg_cena_m2[0:] 
df_Zeme_max_min_avg_cena_m2.columns = new_header2

new_header3 = df_Zeme_max_min_avg_izmers.iloc[0] 
df_Zeme_max_min_avg_izmers = df_Zeme_max_min_avg_izmers[1:] 
df_Zeme_max_min_avg_izmers.columns = new_header3


# Title

st.title('Zemes Cenu pārskats Latvijā')


# Description

st.markdown('Datu analīzes projekts par zemes pārdošanu un cenām Latvijā.')

st.write('[Sludinājumu pārskats](https://ri-oz-zemeanalytics-zemesludinajumuparskats-qa-mzwx0y.streamlit.app)')


st.caption('Made by RIOZ')


# Create a section for the dataframe statistics

st.header('Datu statistiskā analīze')
st.write(df_zeme_clean.describe())

# Create a section for the dataframe
st.header('Sludinājumu dati')


# Slider to filter dataframe by price
Cena_EUR = df_zeme_clean["Cena EUR"].unique().tolist()

min_value = min(Cena_EUR)
max_value = max(Cena_EUR)
value = (min_value, max_value)

Model = st.slider(
    'Cena EUR:',
    min_value=min_value,
    max_value=max_value,
    value=value)

selmin, selmax = Model
selmind = selmin
selmaxd = selmax

dfres = df_zeme_clean.loc[(df_zeme_clean['Cena EUR'] >= selmind) & (df_zeme_clean['Cena EUR'] <= selmaxd)]

st.dataframe(dfres)



# City overview section

st.header('Pilsētu pārskats')

#options = df_Zeme_analytics_Pilseta_skaits['index'].unique().tolist()
#selected_options = st.sidebar.multiselect('Izvēlies pilsētas',options)

#filtered_df_pilsetas = df_Zeme_analytics_Pilseta_skaits[df_Zeme_analytics_Pilseta_skaits["index"].isin(selected_options)]


st.dataframe(df_Zeme_analytics_Pilseta_skaits)

st.bar_chart(df_Zeme_analytics_Pilseta_skaits)


# Type of land overview question

st.header('Zemes Tipi')

st.bar_chart(df_Zeme_analytics_Tips_skaits)

st.dataframe(df_Zeme_analytics_Tips_skaits)


# Prices owerview

st.header('Vidējās Cenas')

st.bar_chart(df_Zeme_max_min_avg_cena_eur)

Cenas_tips = st.radio(
    "Cenas tips",
    ('Pilna cena', 'Cena par m2'))

if Cenas_tips == 'Pilna cena':
    st.dataframe(df_Zeme_max_min_avg_cena_eur)
    
else:
    st.dataframe(df_Zeme_max_min_avg_cena_m2)



# Izmers owerview

st.header('Zemes izmēru pārskats')

st.bar_chart(df_Zeme_max_min_avg_izmers)

st.dataframe(df_Zeme_max_min_avg_izmers)


# %%
