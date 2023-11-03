import plotly
plotly.tools.set_credentials_file(username='ENTER USER NAME HERE', api_key='ENTER API KEY HERE')
import plotly.plotly as py
import plotly.graph_objs as go
# -*- coding: utf-8 -*-
#https://www.kijiji.ca/b-real-estate/winnipeg/c34l1700192
import requests
import bs4
import lxml
import pandas as pd
import datetime
import pytz
from datetime import timedelta





list1 = ["Recently Added:"]
pd.set_option('display.max_rows', 500000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 100000)
pd.set_option('display.max_colwidth',100000)

title = []
date_posted = []


res = requests.get('https://www.winnipegfreepress.com/rss/?path=%2Flocal',stream=True)
soup = bs4.BeautifulSoup(res.text,"lxml")
type(soup)

print(datetime.datetime.now() - timedelta(hours = 1))
title = [x.text for x in soup.find_all(['title'])]
date_posted = [x.text for x in soup.find_all(['pubdate'])]

recent_title = []
recent_posted = []
for x in range(len(date_posted)):
    date = datetime.datetime.strptime(date_posted[x], '%a, %d %b %Y %H:%M:%S CDT')
    if date >= datetime.datetime.now() - timedelta(hours = 1):
        recent_title.append(title[x])
        recent_posted.append(date_posted[x])
        print(x,recent_title,recent_posted)

data=pd.DataFrame({'title' : pd.Series(recent_title),'date':pd.Series(recent_posted)})

data[["title","date"]].to_csv('freepress.csv',index=False, header=False,mode='a')

trace=go.Table(
    header=dict(values=['News', 'Date Posted'],
                line = dict(color='#7D7F80'),
                fill = dict(color='#a1c3d1'),
                align = ['left'] * 5),
    cells=dict(values=[title[1:-1],
                       date_posted[1:]],
               line = dict(color='#7D7F80'),
               fill = dict(color='#EDFAFF'),
               align = ['left'] * 5))

layout = go.Layout(margin=dict(t=0,l=0,r=0,b=0),width=800,autosize=True)
data = [trace]
fig = dict(data=data, layout=layout)
py.plot(fig, filename = 'basic-line',auto_open=False)


