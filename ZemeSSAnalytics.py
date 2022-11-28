

#%%

import pandas as pd

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pygsheets
import streamlit as st
import numpy as np
from datetime import datetime

#%%
 
gc = pygsheets.authorize(service_file='/Users/rioz/Documents/GitHub/ZemeAnalytics/research-python-gs.json')

#open the google spreadsheet

sh = gc.open('Py_land_data')

#select the first sheet 

wks = sh[0]

df_Zeme = pd.DataFrame(wks.get_all_records())



# %%


