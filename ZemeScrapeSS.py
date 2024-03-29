

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


#functions to get adv list from SS for all regaions from all subsites


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
    alltrs = soup.find_all('tr')
    for el in alltrs:
        if 'id' in el.attrs and 'tr_' in el.attrs['id']:
            rows.append(el)
    rows = rows[:-1] # do not need the last one nor do need to store
    return rows


def processPage(url):
    rows = getRows(url)
    mylist = processRows(rows)
    return mylist # could return processRows(rows)


def processPages(urls):
    results = []
    for url in urls:
        results += processPage(url)
        time.sleep(0.1)
    return results


# base url for the scraping process

url = "https://www.ss.lv/lv/real-estate/plots-and-lands/"


#list of ads to process

mylist = processPages(getUrlList(url))

dfmylist = pd.DataFrame(mylist)

adw_list = dfmylist[0].tolist()


# Functions to get adv data

def get_url_text_html(url):
    
    response = requests.get(url)
    soup_adv_text_html = BeautifulSoup(response.text, 'html.parser')
    
    return soup_adv_text_html




def get_ZemePrice(url):
    
    soup_adv_text_html = get_url_text_html(url)
    price_detail_soup = soup_adv_text_html.find(id="tdo_8")
    
    if price_detail_soup == None:
         adv_price = "NA"
    else:
        adv_price = price_detail_soup.get_text()
        
    return adv_price




def get_ZemePielietojums(url):
    
    soup_adv_text_html = get_url_text_html(url)
    pielietojums_detail_soup = soup_adv_text_html.find(id="tdo_228")
    
    if pielietojums_detail_soup == None:
         adv_pielietojums = "NA"
    else:
        adv_pielietojums = pielietojums_detail_soup.get_text()
        
    return adv_pielietojums



def get_Zemeplatiba(url):
    
    soup_adv_text_html = get_url_text_html(url)
    platiba_detail_soup = soup_adv_text_html.find(id="tdo_3")
    
    if platiba_detail_soup == None:
         adv_platiba = "NA"
    else:
        adv_platiba = platiba_detail_soup.get_text()
        
    return adv_platiba



def get_ZemeKnumurs(url):
    
    soup_adv_text_html = get_url_text_html(url)
    Knumurs_detail_soup = soup_adv_text_html.find(id="tdo_1631")
    
    if Knumurs_detail_soup == None:
         adv_Knumurs = "NA"
    else:
        adv_Knumurs = Knumurs_detail_soup.get_text()
        
    return adv_Knumurs



def get_ZemePilseta(url):
    
    soup_adv_text_html = get_url_text_html(url)
    Pilseta_detail_soup = soup_adv_text_html.find(id="tdo_20")
    
    if Pilseta_detail_soup == None:
         adv_Pilseta = "NA"
    else:
        adv_Pilseta = Pilseta_detail_soup.get_text()
        
    return adv_Pilseta



def get_ZemeIela_nosaukums(url):
    
    soup_adv_text_html = get_url_text_html(url)
    Iela_nosaukums_detail_soup = soup_adv_text_html.find(id="tdo_11")
    
    if Iela_nosaukums_detail_soup == None:
         adv_Iela_nosaukums = "NA"
    else:
        adv_Iela_nosaukums = Iela_nosaukums_detail_soup.get_text()
        
    return adv_Iela_nosaukums



def get_datums(url):
    
    soup_adv_text_html = get_url_text_html(url)
    datums_detail_soup = soup_adv_text_html.findAll(text=re.compile('Datums:'))
        
    return datums_detail_soup



def data_collection_date():

    Todaydate = datetime.today().strftime('%Y-%m-%d')

    return Todaydate


# Making lists of data for dataframe columns

Price_list = [get_ZemePrice(i) for i in adw_list]
Iela_list = [get_ZemeIela_nosaukums(i) for i in adw_list]
Pilseta_list = [get_ZemePilseta(i) for i in adw_list]
Pielietojums_list = [get_ZemePielietojums(i) for i in adw_list]
Platiba_list = [get_Zemeplatiba(i) for i in adw_list]
dates_list = [get_datums(i) for i in adw_list]
Knumurs_list = [get_ZemeKnumurs(i) for i in adw_list]


# building dictionary for dataframe

adv_detalas_dictfromlist = {'Link': adw_list, 'Pilseta': Pilseta_list, 'Iela':Iela_list, 'Platiba': Platiba_list, 'Cena': Price_list, 'Zemes Tips': Pielietojums_list, 'Zemes Numurs':Knumurs_list, 'Datums':dates_list}

# building dataframe

df_zeme = pd.DataFrame(adv_detalas_dictfromlist)
df_zeme['Datu iev.']=data_collection_date()

# Dataframe clean up proceses


df_zeme[['Cena EUR','Cena m2']] = df_zeme['Cena'].str.split('€',n=1,expand=True)
df_zeme[['Platiba Daudzums','Platiba Mervieniba']] = df_zeme['Platiba'].str.split(' ',n=1,expand=True)
df_zeme['Cena m2'] = df_zeme['Cena m2'].str.replace('€/m²', '')
df_zeme['Cena m2'] = df_zeme['Cena m2'].str.replace(')', '')
df_zeme['Cena m2'] = df_zeme['Cena m2'].str.replace('(', '')

df_zeme[['Adrese','Iela2']] = df_zeme['Iela'].str.split('[',n=1,expand=True)


df_zeme['Platiba Daudzums'] = pd.to_numeric(df_zeme['Platiba Daudzums'])
df_zeme['Cena m2'] = df_zeme['Cena m2'].str.replace(' ', '')
df_zeme['Cena EUR'] = df_zeme['Cena EUR'].str.replace(' ', '')
df_zeme['Cena EUR'] = pd.to_numeric(df_zeme['Cena EUR'])
df_zeme['Cena m2'] = pd.to_numeric(df_zeme['Cena m2'])

del df_zeme['Platiba']
del df_zeme['Cena']
del df_zeme['Iela']
del df_zeme['Iela2']

df_zeme.dropna(how='any')

#st.dataframe(df_zeme)

#Writing dataframe to google sheets 

#replaces what is there if not empty,run only the first time when new file is generated

#authorization

gc = pygsheets.authorize(service_file='/Users/rioz/Documents/GitHub/ZemeAnalytics/research-python-gs.json')

#open the google spreadsheet

sh = gc.open('Py_land_data')

#select the first sheet 

wks = sh[0]

#update the first sheet with df, starting at cell B2.
 
wks.set_dataframe(df_zeme,(1,1))


# %%
