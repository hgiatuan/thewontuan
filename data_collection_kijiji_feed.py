import requests
import bs4
import pandas as pd
import datetime
from datetime import timedelta
from pytz import timezone
from collections import defaultdict

pd.set_option('display.max_rows', 500000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 100000)
pd.set_option('display.max_colwidth',100000)

res = requests.get('https://www.kijiji.ca/rss-srp-for-sale/winnipeg/c30353001l1700192?ad=offering')
soup = bs4.BeautifulSoup(res.text,"lxml")
latest_kijiji_house_data=defaultdict(list)
publish_kijiji_house_data=defaultdict(list)
kijiji_house_data={"title":[x.text for x in soup.find_all(['title'])[2:]],
                  "date_posted":[x.text for x in soup.find_all(['pubdate'])[1:]],
                  "price":[x.text for x in soup.find_all(['g-core:price'])[:]],
                  "link":[x.text for x in soup.find_all(['guid'])],
                  "long":[x.text for x in soup.find_all(['geo:long'])],
                  "lat":[x.text for x in soup.find_all(['geo:lat'])],
                  "date_cdt":[]
                  }

for x in range(len(kijiji_house_data['date_posted'])):
    time_stamp = kijiji_house_data['date_posted'][x]
    utc = timezone('UTC')
    central = timezone('US/Central')
    published_time = datetime.datetime.strptime(time_stamp, '%a, %d %b %Y %H:%M:%S %Z')
    published_gmt = published_time.replace(tzinfo=utc)
    published_cst = published_gmt.astimezone(central)
    actual_time_published = published_cst.strftime('%a, %d %b %Y %H:%M:%S %Z')
    kijiji_house_data['date_cdt'].append(actual_time_published)

for x in range(len(kijiji_house_data['date_posted'])):
    date = datetime.datetime.strptime(kijiji_house_data['date_cdt'][x], '%a, %d %b %Y %H:%M:%S CDT')
    if date >= datetime.datetime.now() - timedelta(minutes=3600):
        try:
            latest_kijiji_house_data['title'].append(kijiji_house_data['title'][x])
            latest_kijiji_house_data['date_cdt'].append(kijiji_house_data['date_cdt'][x])
            latest_kijiji_house_data['price'].append(kijiji_house_data['price'][x])
            latest_kijiji_house_data['link'].append(kijiji_house_data['link'][x])
            latest_kijiji_house_data['long'].append(kijiji_house_data['long'][x])
            latest_kijiji_house_data['lat'].append(kijiji_house_data['lat'][x])
        except:
            pass

for x in range(len(latest_kijiji_house_data['price'])):
    if x > 1: 
        if float(latest_kijiji_house_data['price'][x]) > 200000:
            publish_kijiji_house_data['title'].append(latest_kijiji_house_data['title'][x])
            publish_kijiji_house_data['date_cdt'].append(latest_kijiji_house_data['date_cdt'][x])
            publish_kijiji_house_data['price'].append(latest_kijiji_house_data['price'][x])
            publish_kijiji_house_data['link'].append(latest_kijiji_house_data['link'][x])
            publish_kijiji_house_data['long'].append(latest_kijiji_house_data['long'][x])
            publish_kijiji_house_data['lat'].append(latest_kijiji_house_data['lat'][x])
            
not_house_index = [index for index, x in enumerate(publish_kijiji_house_data['link']) if not 'https://www.kijiji.ca/v-house-for-sale/' in x]

house_data = pd.DataFrame({ 'House_Price' : pd.Series(publish_kijiji_house_data['price']),
                            'House_Title' : pd.Series(publish_kijiji_house_data['title']),
                            'Post_Date' : pd.Series(publish_kijiji_house_data['date_cdt']),
                            'House_Link' : pd.Series(publish_kijiji_house_data['link']),
                            'House_Long' : pd.Series(publish_kijiji_house_data['long']),
                            'House_Lat': pd.Series(publish_kijiji_house_data['lat'])
                            })

for x in not_house_index:
    house_data.drop(index=x,inplace = True)

house_data[["House_Price","House_Title","Post_Date",'House_Link','House_Long','House_Lat']].to_csv('house_data.csv',index=False, header=False,mode='a')