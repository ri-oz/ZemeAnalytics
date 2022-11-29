import pandas as pd
import streamlit as st
from datetime import datetime


data = {
    'Tips': ['a', 'v', 's', '2022-07-20', '2022-07-21', '2022-07-21'],
    'Sold': [5, 4, 8, 2, 9, 4]
}

df = pd.DataFrame(data)

st.write('### Initial data')
st.dataframe(df)

Sold = df["Sold"].unique().tolist()

min_value = min(Sold)  # str to datetime
max_value = max(Sold)
value = (min_value, max_value)

Model = st.slider(
    'Sold:',
    min_value=min_value,
    max_value=max_value,
    value=value)

selmin, selmax = Model
selmind = selmin
selmaxd = selmax

dfres = df.loc[(df['Sold'] >= selmind) & (df['Sold'] <= selmaxd)]

st.write('### Data from selected date')
st.dataframe(dfres)