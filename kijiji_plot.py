import plotly
plotly.tools.set_credentials_file(username='ENTER USER NAME HERE', api_key='ENTER API KEY HERE')
import plotly.plotly as py
import plotly.graph_objs as go
import sys
import csv as fd
import pandas as pd
import numpy as np
import datetime
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

recent_title = []
recent_posted = []
recent_price=[]

with open('house_data.csv','r') as f:
    reader=fd.DictReader(f)
    for each in reader:
        house_price.append(each['House_Price'])
        house_title.append(each['House_Title'])
        house_date.append(each['Post_Date'])

for x in range(len(house_date)):
    date = datetime.datetime.strptime(house_date[x], '%a, %d %b %Y %H:%M:%S CDT')
    if date >= datetime.datetime.now() - timedelta(hours = 24):
        recent_title.append(house_title[x])
        recent_posted.append(house_date[x])
        recent_price.append(house_price[x])


percentile_list = pd.DataFrame({
    'Price': pd.Series(recent_price),
    'Title': pd.Series(recent_title),
    'Date_Posted': pd.Series(recent_posted)
    })

percentile_list.sort_values(by=['Price','Date_Posted'],inplace=True,ascending=False)
trace=go.Table(
    header=dict(values=['Price','Title', 'Date Posted'],
                line = dict(color='#7D7F80'),
                fill = dict(color='#a1c3d1'),
                align = ['left'] * 5),
    cells=dict(values=[percentile_list['Price'].head(10),
                       percentile_list['Title'].head(10),
                       percentile_list['Date_Posted'].head(10)],
               line = dict(color='#7D7F80'),
               fill = dict(color='#EDFAFF'),
               align = ['left'] * 5))

layout = go.Layout(margin=dict(t=0,l=0,r=0,b=0),width=800,autosize=True)
data = [trace]
fig = dict(data=data, layout=layout)
py.plot(fig, filename = 'house-data',auto_open=True)

