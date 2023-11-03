import plotly
plotly.tools.set_credentials_file(username='ENTER USER NAME HERE', api_key='ENTER API KEY HERE')
import plotly.plotly as py
import plotly.graph_objs as go
import csv as fd
import pandas as pd
import datetime
from datetime import timedelta


pd.set_option('display.max_rows', 500000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 100000)
pd.set_option('display.max_colwidth',100000)

house_price = []
house_title = []
house_date = []
house_long = []
house_lat = [] 

recent_title = []
recent_posted = []
recent_price=[]
recent_long=[]
recent_lat=[]

mapbox_access_token='ENTER MAP BOX TOKEN HERE'

with open('house_data.csv','r') as f:
    reader=fd.DictReader(f)
    for each in reader:
        house_price.append(each['House_Price'])
        house_title.append(each['House_Title'])
        house_date.append(each['Post_Date'])
        house_long.append(each['House_Long'])
        house_lat.append(each['House_Lat'])
        
#Find the last 2 days postings and price.
for x in range(len(house_date)):
    date = datetime.datetime.strptime(house_date[x], '%a, %d %b %Y %H:%M:%S CDT')
    if date >= datetime.datetime.now() - timedelta(days = 2):
        recent_title.append(house_title[x])
        recent_posted.append(house_date[x])
        recent_price.append(house_price[x])
        recent_long.append(house_long[x])
        recent_lat.append(house_lat[x])

percentile_list = pd.DataFrame({
    'Price': pd.Series(recent_price),
    'Title': pd.Series(recent_title),
    'Date_Posted': pd.Series(recent_posted),
    'Long' : pd.Series(recent_long),
    'Lat' : pd.Series(recent_lat)
    })


percentile_list.sort_values(by=['Price','Date_Posted'],inplace=True,ascending=False)


#Plot House Postings Geo - Manitoba
data = [
    go.Scattermapbox(
        lat=percentile_list['Lat'],
        lon=percentile_list['Long'],
        mode='markers',
        text='Price: $'+percentile_list['Price'] + " "+ percentile_list['Title'],
        marker=dict(
            size=5,
            color='rgb(255,255,0)',
            opacity=0.7
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
py.plot(fig, filename = 'Mapbox')
