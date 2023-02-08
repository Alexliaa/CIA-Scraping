#!/usr/bin/env python
# coding: utf-8

# ## Task 3: Population Centers 
# 
# You will use the following link:
# https://www.census.gov/geographies/reference-files/time-series/geo/centers-population.html
# 
# From this link, you will be able to find two distinct links: Centers of Population by State for 2010 and 2020. Once you have those links, access the information on those pages, and plot the populations centers with the information you have. Are there any differences that seem compelling to you?

# #### Firstly, since the information about the center population of 2010 and 2020 are stored in two different URL links, we are supposed to get the URL of each country.

# In[1]:


import pandas as pd
from bs4 import BeautifulSoup
import requests


# In[2]:


url_3 = "https://www.census.gov/geographies/reference-files/time-series/geo/centers-population.html"
center_link = requests.get(url_3)
center_response = BeautifulSoup(center_link.text, "html.parser")

center_link = [i['href'] for i in center_response.find_all('a', attrs = {'role':'menuitem'}, href=True)][:2]


# In[3]:


center_link


# After we got the URL link for 2010 and 2020, let's scrape the links of Centers of Population by State for 2010 and 2020.

# In[4]:


year_name = [2020,2010]
final_link = []
for i in range(2):
    pop_link = requests.get(center_link[i]) 
    year = year_name[i]
    pop_response = BeautifulSoup(pop_link.text, 'html.parser')

    final_link.append(pop_response.find_all('a', attrs = {'name':'Download the Centers of Population by State: %s' % year}, 
                                              href = True)[0]['href'])


# Then we can store the data from links we scraped in a dataframe.

# In[5]:


import io

res_2020 = requests.get(final_link[0])
df_2020 = pd.read_csv(io.StringIO(res_2020.text), sep=',')
df_2020['year'] = 2020

res_2010 = requests.get(final_link[1])
df_2010 = pd.read_csv(io.StringIO(res_2010.text), sep=',')
df_2010['year'] = 2010

total_location = pd.concat([df_2010, df_2020])


# Finally, let's plot the population centers of each state on a map of the US.
# We can find that there is not a significant change based on the location center of populations by states for 2010 and 2020.

# In[6]:


import folium

map = folium.Map(location=[39.8283, -98.5795], zoom_start=4)


for lat, lng, year in zip(total_location['LATITUDE'], total_location['LONGITUDE'], total_location['year']):
    if year == 2010:
        color = 'blue'
    else:
        color = 'red'
    folium.CircleMarker(
        [lat, lng],
        radius=3,
        color=color,
        fill=True,
        fill_color=color
    ).add_to(map)


map


# In[ ]:




