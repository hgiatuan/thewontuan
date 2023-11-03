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

plot_news = pd.read_csv('global_news_categorized.csv')

drop_indexes=[]

for x in range(len(plot_news['date'])): 
    date = datetime.datetime.strptime(plot_news['date'][x], '%a, %d %b %Y %H:%M:%S CDT')
    if date <= datetime.datetime.now() - timedelta(days=30):
        drop_indexes.append(x)

plot_news.drop(plot_news.index[drop_indexes],inplace=True)
plot_news.loc[plot_news[['title','date','area']].duplicated(),['title','date','area']]=''
plot_news.drop(columns=['category'],inplace=True)
plot_news.replace('', np.nan, inplace=True)
plot_news.dropna(inplace=True)
plot_news.loc[plot_news[['title','date']].duplicated(),['title','date']]=''

trace=go.Table(
    header=dict(values=['Title','Area', 'Date Posted'],
                line = dict(color='#7D7F80'),
                fill = dict(color='#a1c3d1'),
                align = ['left'] * 5),
    cells=dict(values=[plot_news['title'],
                       plot_news['area'],
                       plot_news['date']],
               line = dict(color='#7D7F80'),
               fill = dict(color='#EDFAFF'),
               align = ['left'] * 5))

layout = go.Layout(margin=dict(t=0,l=0,r=0,b=0),width=800,autosize=True)
data = [trace]
fig = dict(data=data, layout=layout)
py.plot(fig, filename = 'crime-data',auto_open=True)
