

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

df_tips_mean = df_zeme_clean.groupby(['Zemes Tips']).mean()
df_tips_max = df_zeme_clean.groupby(['Zemes Tips']).max()
df_tips_min = df_zeme_clean.groupby(['Zemes Tips']).min()


df_tips_mean = df_zeme_clean.groupby(['Zemes Tips']).mean()
df_tips_mean = df_tips_mean.add_prefix('Videja ')

df_tips_max = df_zeme_clean.groupby(['Zemes Tips']).max()
df_tips_max = df_tips_max.drop(columns=['Pilseta', 'Platiba Mervieniba','Adrese','Link'])
df_tips_max = df_tips_max.add_prefix('Lielaka ')

df_tips_min = df_zeme_clean.groupby(['Zemes Tips']).min()
df_tips_min = df_tips_min.drop(columns=['Pilseta', 'Platiba Mervieniba','Adrese','Link'])
df_tips_min = df_tips_min.add_prefix('Mazaka ')

df_tips = df_tips_mean.merge(df_tips_max, left_on='Zemes Tips', right_on='Zemes Tips')
df_tips = df_tips.merge(df_tips_min,left_on='Zemes Tips', right_on='Zemes Tips')

del [[df_tips_max,df_tips_min,df_tips_mean]]


df_pilseta_mean = df_zeme_clean.groupby(['Pilseta']).mean()
df_pilseta_mean = df_pilseta_mean.add_prefix('Videja ')

df_pilseta_max = df_zeme_clean.groupby(['Pilseta']).max()
df_pilseta_max = df_pilseta_max.drop(columns=['Zemes Tips', 'Platiba Mervieniba','Adrese','Link'])
df_pilseta_max = df_pilseta_max.add_prefix('Lielaka ')

df_pilseta_min = df_zeme_clean.groupby(['Pilseta']).min()
df_pilseta_min = df_pilseta_min.drop(columns=['Zemes Tips', 'Platiba Mervieniba','Adrese','Link'])
df_pilseta_min = df_pilseta_min.add_prefix('Mazaka ')

df_pilseta = df_pilseta_mean.merge(df_pilseta_max, left_on='Pilseta', right_on='Pilseta')
df_pilseta = df_pilseta.merge(df_pilseta_min,left_on='Pilseta', right_on='Pilseta')

del [[df_pilseta_max,df_pilseta_min,df_pilseta_mean]]


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

st.bar_chart(df_pilseta)

Cenas_tips = st.radio(
    "Datu kategorija",
    ('Pilsetu Dati', 'Pielietojuma dati'))
if Cenas_tips == 'Pilna cena':
    st.dataframe(df_pilseta)
    
else:
    st.dataframe(df_tips)

