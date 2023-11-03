import plotly
plotly.tools.set_credentials_file(username='ENTER USER NAME HERE', api_key='ENTER API HERE')
import plotly.plotly as py
import plotly.graph_objs as go
import requests
import pandas as pd
import datetime
from datetime import timedelta
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


#Getting data in
all_addresses=pd.read_csv("addresses_classified.csv")
posting_info=pd.read_csv("house_data.csv")


#Find the last 7 days postings and price.
for x in range(len(posting_info['Post_Date'])):
    try:
        date = datetime.datetime.strptime(posting_info['Post_Date'][x], '%a, %d %b %Y %H:%M:%S CDT')
        if date > datetime.datetime.now() - timedelta(days = 7) or float(posting_info['House_Price']) > 200000:
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
            

covered_data = pd.DataFrame()
covered_data['date'] = pd.to_datetime(date_cdt)
covered_data['price']= pd.to_numeric(price)

#Find the mean of each day for the last 7 days
covered_data = covered_data.groupby([covered_data['date'].dt.date])['price'].mean()
#After converting it will put dates as indexes, and needs to be seperated as a list of date and price for plotting.

converted_data = pd.DataFrame(covered_data)
converted_data['date'] = converted_data.index

#Plot Average Price Last 7 Days chart
trace = go.Scatter(
    x = converted_data['date'],
    y = converted_data['price']
)

layout = go.Layout(margin=dict(t=50,l=50,r=50,b=50),width=800)
data = [trace]
fig = dict(data=data, layout=layout)
py.plot(fig, filename = 'avg_price_7days',auto_open=False)
