import plotly
plotly.tools.set_credentials_file(username='ENTER USER NAME HERE', api_key='ENTER API HERE')
import plotly.plotly as py
import plotly.graph_objs as go
import requests
import bs4
import lxml
import pandas as pd
import csv as fd
import os
import datetime
from datetime import timedelta
from pytz import timezone
import pytz
import numpy as np


pd.set_option('display.max_rows', 500000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 100000)
pd.set_option('display.max_colwidth',100000)

title = []
price = []
link = []
long = []
lat = []
date_cdt = []
addresses_covered=[]
covered_area=[]

all_addresses=pd.read_csv("addresses_classified.csv")
posting_info=pd.read_csv("house_data.csv")

for x in range(len(posting_info['Post_Date'])):
    try:
        date = datetime.datetime.strptime(posting_info['Post_Date'][x], '%a, %d %b %Y %H:%M:%S CDT')
        if date > datetime.datetime.now() - timedelta(hours = 30) or float(posting_info['House_Price']) > 200000:
            try:
                price.append(posting_info['House_Price'][x])
                title.append(posting_info['House_Title'][x])
                date_cdt.append(posting_info['Post_Date'][x])
                lat.append(posting_info['House_Lat'][x])
                long.append(posting_info['House_Long'][x])
                link.append(posting_info['House_Link'][x])
            except:
                pass
    except:
        pass
            

all_addresses['address'] = all_addresses['address'].str[:-9].astype(str)

#Loops through listing titles and find the specific address of the posting.
#For each house posting title if title is included in all addresses append it to covered area list with the house details and newly added area. 
covered_addresses = [each for each in range(len(title))
                     if any(area.upper() in (title[each]).upper() and covered_area.append(list(zip([title[each]],
                                                                                                           [price[each]],
                                                                                                           [date_cdt[each]],
                                                                                                           [link[each]],
                                                                                                           [long[each]],
                                                                                                           [lat[each]],
                                                                                                           [area]))[0])
                            for area in all_addresses['address'])]


        
covered_data = pd.DataFrame(covered_area,columns=['title','price','date','link','long','lat','area'])
not_house_index = [index for index, x in enumerate(covered_data['link']) if not 'https://www.kijiji.ca/v-house-for-sale/' in x]
#empty_array = [covered_data.drop(index=index,inplace=True) for index, x in enumerate(covered_data['link']) if not 'https://www.kijiji.ca/v-house-for-sale/' in x]

for x in not_house_index:
    covered_data.drop(index=x,inplace = True)
    
#Drop all duplicates    
covered_data.drop_duplicates(subset=['title','area'],inplace=True) 
#Due to one title might have mutiple addresses, make sure everything is duplicated is being replaced by empty spaces
covered_data.loc[covered_data[['title','area','date','price','long','lat']].duplicated(), ['title','area','date','price','long','lat']] = '' 
#Leave out the Area this time and replace the duplicates with empty spaces
covered_data.loc[covered_data[['title','date','price','long','lat']].duplicated(), ['title','date','price','long','lat']] = ''  

trace=go.Table(
    columnwidth = [40,80,250,130],
    header=dict(values=['Price','Area','Title','Date'],
                line =dict(color='#7D7F80'),
                fill = dict(color='#a1c3d1'),
                align = ['left'] * 5),
    cells=dict(values=[
                       covered_data['price'],
                       covered_data['area'],
                       covered_data['title'],
                       covered_data['date']
                       ],
               line = dict(color='#7D7F80'),
               fill = dict(color='#EDFAFF'),
               align = ['left'] * 5))

layout = go.Layout(margin=dict(t=0,l=0,r=0,b=0),width=800,autosize=True)
data = [trace]
fig = dict(data=data, layout=layout)
py.plot(fig, filename = 'area')

