import plotly
plotly.tools.set_credentials_file(username='ENTER USER NAME HERE', api_key='ENTER API KEY HERE')
import plotly.plotly as py
import plotly.graph_objs as go
# -*- coding: utf-8 -*-
#https://www.kijiji.ca/b-real-estate/winnipeg/c34l1700192
import requests
import bs4
from bs4 import CData
import lxml
import pandas as pd
import datetime
import pytz
from datetime import timedelta
from pytz import timezone
import csv as fd
import json
import numpy as np


pd.set_option('display.max_rows', 500000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 100000)
pd.set_option('display.max_colwidth',100000)

addresses=[]
neighbourhood=[]
community=[]
river=[]
lake=[]

title = []
date_posted = []
date_cdt=[]

covered_area=[]
area=[]


news_title =[]
news_date=[]
news_category=[]

recent_title = []
recent_posted = []
recent_category = []

news_data=[]
news_real_data=[]

categories_extracted_news = []
with open('mb_wp_street_name.csv','r') as f:
    reader=fd.DictReader(f)
    for each in reader:
        addresses.append(each['addresses'])
with open('mb_community_area.csv','r',encoding="utf8",errors='ignore') as f:
    reader=fd.DictReader(f)
    for each in reader:
        community.append(each['community'])
with open('mb_neighbourhood_area.csv','r',encoding="utf8",errors='ignore') as f:
    reader=fd.DictReader(f)
    for each in reader:
        neighbourhood.append(each['neighbourhood'])
with open('mb_lake.csv','r') as f:
    reader=fd.DictReader(f)
    for each in reader:
        lake.append(each['lake'])
with open('mb_river.csv','r') as f:
    reader=fd.DictReader(f)
    for each in reader:
        river.append(each['river'])


map_request_url="https://maps.googleapis.com/maps/api/geocode/json"

params=[]

all_addresses = addresses + community + neighbourhood + river + lake

all_addresses_mod =[each + " Manitoba" for each in all_addresses]
for each in all_addresses_mod:
    params.append({'sensor': 'false', 'address': str(each),"components":"country:Canada",'key':'AIzaSyDn1ASa287uH-SnZw1AgbFz5s_4IZQS7zM'})

    

long=[]
lat=[]
addresses=[]
new_address=[]
for each in params:
    try:
        r = requests.get(map_request_url, params=each,)
        results = r.json()['results']
        #print(json.dumps(results ,indent=4,sort_keys=True))
        location = results[0]['geometry']['location']
        long.append(location['lng'])
        lat.append(location['lat'])
        addresses.append(each['address'])
        new_address.append(results[0]["formatted_address"])
    except:
        pass




classified_addresses = pd.DataFrame({'address':pd.Series(addresses),'mod_address':pd.Series(new_address),'long':pd.Series(long),'lat':pd.Series(lat)})
print(classified_addresses)

classified_addresses[['address','mod_address','long','lat']].to_csv('addresses_classified.csv',index=False,header=True,mode='a')

