

# %%
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import re

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pygsheets
import streamlit as st
import numpy as np
from datetime import datetime





def getUrlList(url, prefix='https://www.ss.com', postfix='sell/', tag='a', class_='a_category'):
    req = requests.get(url)
    if req.status_code != 200:
        print(f'Unexpected status code {req.status_code}. Stopping parse')
        return [] 
    soup = BeautifulSoup(req.text, 'lxml')
    return [ prefix + el['href'] + postfix for el in soup.find_all(tag, class_) ]
    
    

def processRow(row, baseurl='https://www.ss.com'):
    ritems = []
    tds = row.find_all('td')
    ritems.append(baseurl + tds[1].a['href'])
    ritems.append(tds[2].text.strip().replace('\r','').replace('\n', ''))
    for td in tds[3:-1]:
        ritems.append(td.text)
    ritems.append(int(tds[-1].text.split()[0].replace(',','')))
    ritems.append(tds[-1].text.split()[1])
    return ritems

def processRows(rows):
    rowlist=[]
    for row in rows:
        rowlist.append(processRow(row))
    return rowlist


def getRows(url):
    req = requests.get(url)
    rows = []
    if req.status_code != 200:
        print("Bad Request"+req.status_code)
        return
    soup = BeautifulSoup(req.text, 'lxml')
    print("Processing: "+ str(soup.title))
    # this will be specific to ss.lv and ss.com
    alltrs = soup.find_all('tr')
    for el in alltrs:
        if 'id' in el.attrs and 'tr_' in el.attrs['id']:
            rows.append(el)
    rows = rows[:-1] # we do not need the last one nor do we need to store
    return rows


def processPage(url):
    rows = getRows(url)
    mylist = processRows(rows)
    return mylist # could return processRows(rows)


def processPages(urls):
    results = []
    for url in urls:
        print("Processing: "+url)
        results += processPage(url)
        time.sleep(0.1)
    return results


url = "https://www.ss.lv/lv/real-estate/plots-and-lands/"


mylist = processPages(getUrlList(url))

dfmylist = pd.DataFrame(mylist)

adw_list = dfmylist[0].tolist()


def get_ZemePrice(url):
    
    response = requests.get(url)
    soup_adv_text_html = BeautifulSoup(response.text, 'html.parser')
    price_detail_soup = soup_adv_text_html.find(id="tdo_8")
    
    if price_detail_soup == None:
         adv_price = "NA"
    else:
        adv_price = price_detail_soup.get_text()
        
    return adv_price




def get_ZemePielietojums(url):
    
    response = requests.get(url)
    soup_adv_text_html = BeautifulSoup(response.text, 'html.parser')
    pielietojums_detail_soup = soup_adv_text_html.find(id="tdo_228")
    
    if pielietojums_detail_soup == None:
         adv_pielietojums = "NA"
    else:
        adv_pielietojums = pielietojums_detail_soup.get_text()
        
    return adv_pielietojums



def get_Zemeplatiba(url):
    
    response = requests.get(url)
    soup_adv_text_html = BeautifulSoup(response.text, 'html.parser')
    platiba_detail_soup = soup_adv_text_html.find(id="tdo_3")
    
    if platiba_detail_soup == None:
         adv_platiba = "NA"
    else:
        adv_platiba = platiba_detail_soup.get_text()
        
    return adv_platiba



def get_ZemeKnumurs(url):
    
    response = requests.get(url)
    soup_adv_text_html = BeautifulSoup(response.text, 'html.parser')
    Knumurs_detail_soup = soup_adv_text_html.find(id="tdo_1631")
    
    if Knumurs_detail_soup == None:
         adv_Knumurs = "NA"
    else:
        adv_Knumurs = Knumurs_detail_soup.get_text()
        
    return adv_Knumurs



def get_ZemePilseta(url):
    
    response = requests.get(url)
    soup_adv_text_html = BeautifulSoup(response.text, 'html.parser')
    Pilseta_detail_soup = soup_adv_text_html.find(id="tdo_20")
    
    if Pilseta_detail_soup == None:
         adv_Pilseta = "NA"
    else:
        adv_Pilseta = Pilseta_detail_soup.get_text()
        
    return adv_Pilseta



def get_ZemeIela_nosaukums(url):
    
    response = requests.get(url)
    soup_adv_text_html = BeautifulSoup(response.text, 'html.parser')
    Iela_nosaukums_detail_soup = soup_adv_text_html.find(id="tdo_11")
    
    if Iela_nosaukums_detail_soup == None:
         adv_Iela_nosaukums = "NA"
    else:
        adv_Iela_nosaukums = Iela_nosaukums_detail_soup.get_text()
        
    return adv_Iela_nosaukums



def get_datums(url):
    
    response = requests.get(url)
    soup_adv_text_html = BeautifulSoup(response.text, 'html.parser')
    datums_detail_soup = soup_adv_text_html.findAll(text=re.compile('Datums:'))
        
    return datums_detail_soup



def data_collection_date():

    Todaydate = datetime.today().strftime('%Y-%m-%d')

    return Todaydate




Price_list = [get_ZemePrice(i) for i in adw_list]
Iela_list = [get_ZemeIela_nosaukums(i) for i in adw_list]
Pilseta_list = [get_ZemePilseta(i) for i in adw_list]
Pielietojums_list = [get_ZemePielietojums(i) for i in adw_list]
Platiba_list = [get_Zemeplatiba(i) for i in adw_list]
dates_list = [get_datums(i) for i in adw_list]
Knumurs_list = [get_ZemeKnumurs(i) for i in adw_list]


adv_detalas_dictfromlist = {'Link': adw_list, 'Pilseta': Pilseta_list, 'Iela':Iela_list, 'Platiba': Platiba_list, 'Cena': Price_list, 'Zemes Tips': Pielietojums_list, 'Zemes Numurs':Knumurs_list, 'Datums':dates_list}

df_zeme = pd.DataFrame(adv_detalas_dictfromlist)
df_zeme['Datu iev.']=data_collection_date()



#st.dataframe(df_zeme)



# %%

#Writing dataframe to google sheets 

#replaces what is there if not empty,run only the first time when new file is generated

#authorization

#gc = pygsheets.authorize(service_file='/Users/rioz/Documents/GitHub/ZemeAnalytics/research-python-gs.json')

#open the google spreadsheet

#sh = gc.open('Py_land_data')

#select the first sheet 

#wks = sh[0]

#update the first sheet with df, starting at cell B2.
 
#wks.set_dataframe(df_zeme,(1,1))




#%%

#Google Sheets append part 


from __future__ import print_function
from auth.CAS.REST.service import api
from pprint import pprint
from googleapiclient import discovery

#%%

# The ID of the spreadsheet to update.
spreadsheet_id = '1karOXhe5kVN1dTJTCeNsKg4QHuqOZ80LPx-YRV--2fE'  # TODO: Update placeholder value.

# The A1 notation of a range to search for a logical table of data.
# Values will be appended after the last row of the table.
range_ = 'A:I'  # TODO: Update placeholder value.

# How the input data should be interpreted.
value_input_option = 'RAW'  # TODO: Update placeholder value.

# How the input data should be inserted.
insert_data_option = 'INSERT_ROWS'  # TODO: Update placeholder value.

df_values = df_zeme.values.tolist()

value_range_body = {df_values}

request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
response = request.execute()


# %%
