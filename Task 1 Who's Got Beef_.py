#!/usr/bin/env python
# coding: utf-8

# ## Task 1: Who's Got Beef?
# ### The CIA has a running tab on international boundary disputes: 
# https://www.cia.gov/the-world-factbook/field/disputes-international. 
# Which countries seem to be involved in the most land disputes?

# In[2]:


beef_link = requests.get('https://www.cia.gov/the-world-factbook/field/disputes-international')
beef_name = BeautifulSoup(beef_link.content, 'html.parser')


# Firstly, let's scrape country names and the content of disputes of each country and store them in a data frame.

# In[3]:


# scrape country names
country_name = beef_name.select("h2")

# scrape the content of disputes of each country
country_beef = beef_name.select('li')[4:261]


# In[4]:


table_names = []
table_beef = []

# store them in two lists
for i in range(len(country_name)):
    table_names.append(country_name[i].getText())
    
for i in range(len(country_beef)):
    table_beef.append(country_beef[i].getText())

# combine these two lists into a dataframe    
country_df = pd.DataFrame([table_beef], columns = table_names).T
country_df.rename(columns = {0:'beef'}, inplace = True)


# In[5]:


# slice the contents to remove the first country names which are redundant.
for i in range(len(country_df)):
    country_df.iloc[i,0] = country_df.iloc[i,0][len(table_names[i]):]


# Notes that there are punctuations like ':',':', and '()' in dispute contents, so let's clean the text by regular expression.

# In[6]:


country_df['beef'] = country_df.beef.str.replace('[-:.?()]', ' ', regex=True)
country_df['beef'] = country_df.beef.str.split('(?=[A-Z][a-z])').str.join(' ')

#since EU is not a country, we are supposed to remove it.
country_df.drop(index = 'European Union', inplace = True)


# Then we are going to split the content and store them in a list. Each value in the contry_list is a list that stores the words in the dispute content of each country.

# In[7]:


import re

country_list = []
for i in range(len(country_df)):
    country_list.append(list(set(re.split('[\s-]', country_df['beef'][i]))))


# After this, Let's count how many country names appear in each country's dspute content.

# In[8]:


from collections import Counter
import pycountry

names = []
abb = []
for country in pycountry.countries:
        names.append(country.name)
        abb.append(country.alpha_2)
names = names + abb + list(country_df.index)

counter1 = Counter(names)
table_number = []
for i in range(len(country_list)):
    counter2 = Counter(country_list[i])
    table_number.append(sum((counter1 & counter2).values()))


# #### Finally, let's add the number of disputes into our dataframe.
# Before that, there is one last step. Since we counted each country's name as a dispute, we need to subtract one for each number that is greater than 1.

# In[9]:


table_number = [i-1 if i > 0 else i for i in table_number]

country_df['#disputes'] = table_number
country_df.sort_values('#disputes', ascending = False).head(10)

