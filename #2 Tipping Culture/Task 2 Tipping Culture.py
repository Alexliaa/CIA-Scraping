#!/usr/bin/env python
# coding: utf-8

# ## Task 2: Tipping Culture
# 
# The CIA also publishes information about 262 countries: https://www.cia.gov/the-world-factbook/countries/. Use the page's API to randomly select 20 countries and report on the tipping cultures in those countries. You can find that information in the Travel Facts page for each country.
# 
# 

# In[10]:


import json

url = 'https://www.cia.gov/the-world-factbook/page-data/countries/page-data.json'

response = requests.get(url)
ct_ls = json.loads(response.text)['result']['data']['countries']['edges']


country_ls = [i['node']['title'] for i in ct_ls]


# We have got the list of country names in the code above, then we can randomly select 20 countries.

# In[11]:


import random

random.seed(7)
lucky_country = random.sample(country_ls, 20)

#convert them to the standard form of url link.
lucky_countrys = [c.replace(' ','-').replace(',','-').lower() for c in lucky_country]
lucky_countrys


# In[12]:


url_2 = 'https://www.cia.gov/the-world-factbook/countries/'

tipping_ls = []
for country in lucky_countrys:
    title_ls = []
    content_ls = []
    country_link = requests.get(url_2 + str(country) + '/travel-facts')#get the url link of travel facts page.
    
    #Since some countres don't have travel facts page, we need to find them.
    if country_link.status_code == 404:
        tipping_ls.append('None')
        print(f'{country} does not have Travel Facts page')
    else:
        country_response = BeautifulSoup(country_link.text, 'html.parser')
        title = country_response.find_all('h3' ,attrs = {'mt30'})#get titles of all the travel facts
        content = country_response.select('p')[:len(title)]#get content of all the travel facts

        for i in range(len(title)):
            title_ls.append(title[i].getText())
            content_ls.append(content[i].getText())   
        tipping_ls.append(content_ls[title_ls.index('Tipping Guidelines')])#get the content of Tipping Guidelines


# In[13]:


dict(zip(lucky_country, tipping_ls))


# In[ ]:


## Task 2: Tipping Culture

The CIA also publishes information about 262 countries: https://www.cia.gov/the-world-factbook/countries/. Use the page's API to randomly select 20 countries and report on the tipping cultures in those countries. You can find that information in the Travel Facts page for each country.



import json

url = 'https://www.cia.gov/the-world-factbook/page-data/countries/page-data.json'

response = requests.get(url)
ct_ls = json.loads(response.text)['result']['data']['countries']['edges']


country_ls = [i['node']['title'] for i in ct_ls]

We have got the list of country names in the code above, then we can randomly select 20 countries.

import random

random.seed(7)
lucky_country = random.sample(country_ls, 20)

#convert them to the standard form of url link.
lucky_countrys = [c.replace(' ','-').replace(',','-').lower() for c in lucky_country]
lucky_countrys

url_2 = 'https://www.cia.gov/the-world-factbook/countries/'

tipping_ls = []
for country in lucky_countrys:
    title_ls = []
    content_ls = []
    country_link = requests.get(url_2 + str(country) + '/travel-facts')#get the url link of travel facts page.
    
    #Since some countres don't have travel facts page, we need to find them.
    if country_link.status_code == 404:
        tipping_ls.append('None')
        print(f'{country} does not have Travel Facts page')
    else:
        country_response = BeautifulSoup(country_link.text, 'html.parser')
        title = country_response.find_all('h3' ,attrs = {'mt30'})#get titles of all the travel facts
        content = country_response.select('p')[:len(title)]#get content of all the travel facts

        for i in range(len(title)):
            title_ls.append(title[i].getText())
            content_ls.append(content[i].getText())   
        tipping_ls.append(content_ls[title_ls.index('Tipping Guidelines')])#get the content of Tipping Guidelines

dict(zip(lucky_country, tipping_ls))

