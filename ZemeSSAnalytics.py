

#%%

import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pygsheets
import streamlit as st
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

 
gc = pygsheets.authorize(service_file='/Users/rioz/Documents/GitHub/ZemeAnalytics/research-python-gs.json')

#open the google spreadsheet

sh = gc.open('Py_land_data')

#select the first sheet 

wks = sh[0]

# create dataframe

df_Zeme = pd.DataFrame(wks.get_all_records())

#df_Zeme_analytics_Cena_bins = df_Zeme['Cena EUR'].value_counts(bins=20)

df_Zeme_analytics_Pilseta_skaits = df_Zeme['Pilseta'].value_counts(ascending=True)

df_Zeme_analytics_Tips_skaits = df_Zeme['Zemes Tips'].value_counts(ascending=True)


# Title

st.title('Zemes Cenu pārskats Latvijā')


# Description

st.text('Datu analīzes projekts par zemes pārdošanu un cenām Latvijā.')


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

