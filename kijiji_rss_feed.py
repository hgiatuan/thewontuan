import requests
import bs4
import lxml
import pandas as pd
import os
import datetime
from datetime import timedelta
from pytz import timezone
import pytz

i = 0
list1 = ["Recently Added:"]
pd.set_option('display.max_rows', 500000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 100000)
pd.set_option('display.max_colwidth',100000)

title = []
price = []
date_posted = []
link =[]
long = []
lat = []
  

res = requests.get('https://www.kijiji.ca/rss-srp-for-sale/winnipeg/c30353001l1700192?ad=offering')
soup = bs4.BeautifulSoup(res.text,"lxml")
type(soup)
title = [x.text for x in soup.find_all(['title'])[2:]]
date_posted = [x.text for x in soup.find_all(['pubdate'])[1:]]
price = [x.text for x in soup.find_all(['g-core:price'])[:]]
link = [x.text for x in soup.find_all(['guid'])]
long = [x.text for x in soup.find_all(['geo:long'])]
lat = [x.text for x in soup.find_all(['geo:lat'])]

print(date_posted)
    
recent_title = []
recent_posted = []
recent_price=[]
recent_link=[]
recent_long = []
recent_lat = []
date_cdt = []

house_price = []
house_title= []
house_date=[]
house_link=[]
house_lat=[]
house_long=[]

for x in range(len(date_posted)):
    time_stamp = date_posted[x]
    utc = timezone('UTC')
    central = timezone('US/Central')
    published_time = datetime.datetime.strptime(time_stamp, '%a, %d %b %Y %H:%M:%S %Z')
    published_gmt = published_time.replace(tzinfo=utc)
    published_cst = published_gmt.astimezone(central)
    actual_time_published = published_cst.strftime('%a, %d %b %Y %H:%M:%S %Z')
    date_cdt.append(actual_time_published)

for x in range(len(date_posted)):
    date = datetime.datetime.strptime(date_cdt[x], '%a, %d %b %Y %H:%M:%S CDT')
    if date >= datetime.datetime.now() - timedelta(minutes=600):
        try:
            print(title[x])
            recent_title.append(title[x])
            recent_posted.append(date_cdt[x])
            recent_price.append(price[x])
            recent_link.append(link[x])
            recent_long.append(long[x])
            recent_lat.append(lat[x])
        except:
            pass
            
for x in range(len(recent_price)):
    if x > 1: 
        if float(recent_price[x]) > 200000:
            house_price.append(recent_price[x])
            house_date.append(recent_posted[x])
            house_title.append(recent_title[x])
            house_link.append(recent_link[x])
            house_long.append(recent_long[x])
            house_lat.append(recent_lat[x])
    
percentile_list = pd.DataFrame({
    'Price': pd.Series(recent_price[:]),
    'Title': pd.Series(recent_title[:]),
    'Date_Posted': pd.Series(recent_posted[:]),
    'Link' : pd.Series(recent_link)
    })

print(percentile_list)
print(datetime.datetime.now())
not_house_index = [index for index, x in enumerate(house_link) if not 'https://www.kijiji.ca/v-house-for-sale/' in x]


house_data = pd.DataFrame({ 'House_Price' : pd.Series(house_price),
                            'House_Title' : pd.Series(house_title),
                            'Post_Date' : pd.Series(house_date),
                            'House_Link' : pd.Series(house_link),
                            'House_Long' : pd.Series(house_long),
                            'House_Lat': pd.Series(house_lat)
                            })

for x in not_house_index:
    house_data.drop(index=x,inplace = True)

house_data[["House_Price","House_Title","Post_Date",'House_Link','House_Long','House_Lat']].to_csv('house_data.csv',index=False, header=False,mode='a')

