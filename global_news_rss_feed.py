import plotly
plotly.tools.set_credentials_file(username='tuanhuynh', api_key='ULhrfpMgmhU5mx10DPCP')
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


all_addresses = addresses + community + neighbourhood + river + lake

#Collecting Global News RSS Feeds
res = requests.get('https://globalnews.ca/tag/winnipeg-crime/feed/',stream=True)
soup = bs4.BeautifulSoup(res.text,'html.parser')


item=[x for x in soup.find_all(['item'])]

for each in item:
    news_category.append([x.text for x in each.findAll('category')])
    news_title.append([x.text for x in each.findAll('title')])
    news_date.append([x.text for x in each.findAll('pubdate')])

for each in range(len(item)):
    date_posted.append(news_date[each][0])
    title.append(news_title[each][0])

for x in range(len(date_posted)):
    time_stamp = date_posted[x].strip('+0000') + 'UTC'
    utc = timezone('UTC')
    central = timezone('US/Central')
    published_time = datetime.datetime.strptime(time_stamp, '%a, %d %b %Y %H:%M:%S %Z')
    published_gmt = published_time.replace(tzinfo=utc)
    published_cst = published_gmt.astimezone(central)
    actual_time_published = published_cst.strftime('%a, %d %b %Y %H:%M:%S %Z')
    date_cdt.append(actual_time_published)
    
for x in range(len(date_cdt)):
    date = datetime.datetime.strptime(date_cdt[x], '%a, %d %b %Y %H:%M:%S CDT')
    if date >= datetime.datetime.now() - timedelta(hours=24):
        recent_title.append(title[x])
        recent_posted.append(date_cdt[x])
        recent_category.append(news_category[x])

data=pd.DataFrame({'title' : pd.Series(recent_title[:]),
                   'date':pd.Series(recent_posted),
                   'category':pd.Series(recent_category),
                   'area':pd.Series('')})

#Mapping each news header title to multiple categories
for each in range(len(data['title'])):
    for x in data['category'][each]:
        #zip all data together and unzip it into a list to come an array of tuples
        news_real_data.append(list(zip([data['title'][each]],
                                       [data['date'][each]],
                                       [x],
                                       [data['area'][each]],
                                       [data['category'][each]]))[0])
    
news_df = pd.DataFrame(news_real_data,columns=['title','date','category','area','tag'])


#Searching for area that contain within all addresses
search_address=[each for each in range(len(news_df['category']))
                if any(word.upper() in news_df['category'][each].upper()
                       and covered_area.append(
                           list(zip([news_df['title'][each]],
                                   [news_df['date'][each]],
                                   [news_df['tag'][each]],
                                   [word]))[0])
                       for word in all_addresses)]


df=pd.DataFrame(covered_area,columns=['title','date','tag','area'])

for each in range(len(df['title'])):
    for x in df['tag'][each]:
        categories_extracted_news.append(list(zip(
            [df['title'][each]],
            [df['date'][each]],
            [x],
            [df['area'][each]]))[0])

global_news_categorized=pd.DataFrame(categories_extracted_news,columns=['title','date','category','area'])
global_news_categorized[['title','date','category','area']].to_csv('global_news_categorized.csv',index=False,header=False,mode='a')

