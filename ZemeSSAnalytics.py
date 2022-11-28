

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

df_Zeme = pd.read_csv(url, index_col=0)

# Drop error / na rows

df_Zeme.dropna(how='any')

#df_Zeme = pd.DataFrame(wks.get_all_records())

#df_Zeme_analytics_Cena_bins = df_Zeme['Cena EUR'].value_counts(bins=20)

df_Zeme_analytics_Pilseta_skaits = df_Zeme['Pilseta'].value_counts(ascending=True)

df_Zeme_analytics_Tips_skaits = df_Zeme['Zemes Tips'].value_counts(ascending=True)

df_Zeme_max_min_avg_cena_eur = df_Zeme.groupby('Pilseta').agg({'Cena EUR': ['mean', 'min', 'max']})
df_Zeme_max_min_avg_cena_m2 = df_Zeme.groupby('Pilseta').agg({'Cena m2': ['mean', 'min', 'max']})

df_Zeme_max_min_avg_izmers = df_Zeme.groupby('Pilseta').agg({'Platiba Daudzums': ['mean', 'min', 'max']})



# Title

st.title('Zemes Cenu pārskats Latvijā')


# Description

st.markdown('Datu analīzes projekts par zemes pārdošanu un cenām Latvijā.')


# Create a section for the dataframe statistics

st.header('Datu statistiskā anaīze')
st.write(df_Zeme.describe())

# Create a section for the dataframe
st.header('Sludinājumu dati')
st.dataframe(df_Zeme)


# City overview section

st.header('Pilsētu pārskats')

st.bar_chart(df_Zeme_analytics_Pilseta_skaits)

st.dataframe(df_Zeme_analytics_Pilseta_skaits)


# Type of land overview question

st.header('Zemes Tipi')

st.bar_chart(df_Zeme_analytics_Tips_skaits)

st.dataframe(df_Zeme_analytics_Tips_skaits)


# Prices owerview

st.header('Videjās Cenas')

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


