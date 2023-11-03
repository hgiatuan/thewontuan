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
mapbox_access_token=''
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

all_addresses=pd.read_csv("addresses_classified.csv")
all_addresses['address'] = all_addresses['address'].str[:-9].astype(str)
long = dict(zip(all_addresses['address'],all_addresses['long']))
lat= dict(zip(all_addresses['address'],all_addresses['lat']))

plot_long=[]
plot_lat=[]
plot_area=[]
plot_title=[]
plot_date=[]

for each in plot_news['area']:
    plot_long.append(long[each])
    plot_lat.append(lat[each])
    


data = [
    go.Scattermapbox(
        lat=plot_lat,
        lon=plot_long,
        mode='markers',
        text='News: '+plot_news['title']+ "<br>"+ plot_news['area'] + "<br>" + plot_news['date'],
        name="Crime Scenes",
        marker=dict(
            size=20,
            color='rgb(255,0,0)',
            opacity=0.2
        ),
    )]

layout = go.Layout(
    autosize=True,
    hovermode='closest',
    margin=dict(t=0,l=0,r=0,b=0),
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=49.8951,
            lon=-97.1384
        ),
        pitch=0,
        zoom=7,
        style='dark'
    ),
)

fig = dict(data=data, layout=layout)
py.plot(fig, filename = 'crime_map')

