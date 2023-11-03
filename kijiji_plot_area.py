import plotly
plotly.tools.set_credentials_file(username='ENTER USER NAME HERE', api_key='ENTER API KEY HERE')
import plotly.plotly as py
import plotly.graph_objs as go
import sys
import csv as fd
import pandas as pd
import numpy as np
import datetime
from datetime import timedelta
from pytz import timezone
import pytz

pd.set_option('display.max_rows', 500000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 100000)
pd.set_option('display.max_colwidth',100000)

house_price = []
house_title = []
house_date = []
house_lat=[]
house_long=[]
house_link=[]
addresses=[]
neighbourhood=[]
community=[]
lake=[]
river=[]

recent_title = []
recent_posted = []
recent_price=[]
recent_long=[]
recent_lat=[]
recent_link=[]
area_exist =[]

covered_title = []
covered_date = []
covered_price= []
covered_lat=[]
covered_long=[]
covered_link=[]
with open('house_data.csv','r') as f:
    reader=fd.DictReader(f)
    for each in reader:
        house_price.append(each['House_Price'])
        house_title.append(each['House_Title'])
        house_date.append(each['Post_Date'])
        house_lat.append(each['House_Lat'])
        house_long.append(each['House_Long'])
        house_link.append(each['House_Link'])
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

for x in range(len(house_date)):
    date = datetime.datetime.strptime(house_date[x], '%a, %d %b %Y %H:%M:%S CDT')
    if date >= datetime.datetime.now() - timedelta(days = 7):
        recent_title.append(house_title[x])
        recent_posted.append(house_date[x])
        recent_price.append(house_price[x])
        recent_lat.append(house_lat[x])
        recent_long.append(house_long[x])
        recent_link.append(house_link[x])
        

covered_area=[]
def remember(word):
    covered_area.append(word)
index_list=[]     
def index(index):
    index_list.append(index)

all_addresses = addresses + community + neighbourhood + river + lake

house_address= [x for x in house_title if index(any(word in x for word in all_addresses))]
covered_addresses = [string for string in house_title if any(word in string and remember(word) for word in all_addresses)]
print(covered_addresses)
for index,x in enumerate(index_list):
    if x == True:
        covered_title.append(recent_title[index])
        covered_price.append(recent_price[index])
        covered_date.append(recent_posted[index])
        covered_link.append(recent_link[index])
        covered_lat.append(recent_lat[index])
        covered_long.append(recent_long[index])

percentile_list = pd.DataFrame({
    'Price': pd.Series(covered_price),
    'Title': pd.Series(covered_title),
    'Date_Posted': pd.Series(covered_date),
    'Long':pd.Series(covered_long),
    'Lat':pd.Series(covered_lat),
    'Link':pd.Series(covered_link),
    'Area' : pd.Series(covered_area)
    })

percentile_list.sort_values(by=['Price','Date_Posted'],inplace=True,ascending=False)

trace=go.Table(
    header=dict(values=['Area'],
                line =dict(color='#7D7F80'),
                fill = dict(color='#a1c3d1'),
                align = ['left'] * 5),
    cells=dict(values=[
                       covered_area
                       ],
               line = dict(color='#7D7F80'),
               fill = dict(color='#EDFAFF'),
               align = ['left'] * 5))

layout = go.Layout(margin=dict(t=0,l=0,r=0,b=0),width=800,autosize=True)
data = [trace]
fig = dict(data=data, layout=layout)
py.plot(fig, filename = 'area')

