#!/usr/bin/env python
# coding: utf-8

# ## Web Scraping for RBI

# In[1]:


import requests
import pandas as pd
from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import numpy as np
import nltk
import requests
import pandas as pd
from bs4 import BeautifulSoup
from requests import get
import pandas as pd
#import selenium
from datetime import date, timedelta


# In[2]:


headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}


# In[3]:


html_content = get('https://rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx',headers=headers)


# In[4]:


soup = BeautifulSoup(html_content.text, 'html.parser')


# In[5]:


check = soup.find_all('a',class_="link2")
len(check)


# In[6]:


headings = soup.find_all('a',class_="link2")
urls = []
list_headings = []
for heading in headings:
    #if 'penalty' in heading.text or 'Penalty' in heading.text :
        # print(heading.text)
        list_headings.append(heading.text)
        # list_headings_.append(heading.text)
        
        complete_url = 'https://rbi.org.in/Scripts/'+heading.get('href')
        # print(complete_url)
        urls.append(complete_url)
        # urls_.append(complete_url)


# In[7]:


html_content = get(urls[0],headers=headers)
soup = BeautifulSoup(html_content.text, 'html.parser')


# In[8]:


text_data = []
dates = []
for url in urls:
    html_content = get(url,headers=headers)
    soup = BeautifulSoup(html_content.text, 'html.parser')

    # dates
    date_elements = soup.find_all('td', class_='tableheader')
    for element in date_elements:
        if 'Date :' in element.get_text():
            date_text = element.get_text().replace('Date : ', '').strip()
            dates.append([date_text])

    # Notice_data
    raw_text = soup.find_all('p')
    concat_text = ''
    for text in raw_text:
        concat_text += text.text
    text_data.append([concat_text])


# In[9]:


df = pd.DataFrame({
    'date': dates ,
    'Headings': list_headings,
    'Link': urls,
    'text_data': text_data
})


# In[10]:


def extract(x):
    return x[0]


# In[11]:


df.date = df.date.apply(extract)


# In[12]:


df.text_data = df.text_data.apply(extract)


# In[13]:


df['dates'] = df['date'].apply(lambda x: pd.to_datetime(x))


# In[14]:


df


# In[15]:


df.drop(columns=['date'],axis=1,inplace=True)


# In[16]:


df['text_data'].replace('', np.nan, inplace=True)


# In[17]:


df.dropna(axis=0, subset=['text_data'], thresh=1, inplace=True)


# In[29]:


today = date.today()
Fourdays_before = today - timedelta(days=2)
Fourdays_before = Fourdays_before.strftime('%Y-%m-%d')


# In[30]:


twodays_before


# In[31]:


df1= df[df.dates > Fourdays_before]


# In[32]:


df1


# In[33]:


df1['char_count'] = df['text_data'].str.len()


# In[34]:


df1


# In[35]:


df_final = df1[df1['char_count'] > 400]


# In[36]:


# Dropping columns having Non English or Junk Values

from langdetect import detect, DetectorFactory


# In[37]:


# Set seed for consistent results
DetectorFactory.seed = 0


# In[38]:


def is_english(text):
    try:
        return detect(text) == 'en'
    except:
        return False


# In[39]:


# Apply the function to the DataFrame
df_final['is_english'] = df_final['text_data'].apply(is_english)


# In[40]:


df_final


# In[41]:


df_final = df_final[df_final['is_english'] == True]


# In[42]:


df_final.drop(columns=['is_english'],axis=1,inplace=True)


# In[43]:


df_final.drop(columns=['char_count'],axis=1,inplace=True)


# In[44]:


df_final


# In[45]:


# df1.to_csv('RBI.csv', mode='w',index=False,encoding='utf-8-sig')
df_final.to_csv('RBI.csv', mode='w',index=False,encoding='utf-8')


# ## Web Scrapping for PIB

# In[46]:


html_content = get('https://pib.gov.in/allRel.aspx',headers=headers)


# In[47]:


soup = BeautifulSoup(html_content.text, 'html.parser')


# In[48]:


urls = []
titles = []
urls_html = soup.find_all('ul',class_='num')
for url in urls_html:

    x = url.find_all('li')
    # print(x)

    for i in x:
        # print(i)
        z = i.find_all('a')
        # print(z)
        
        for a in z:
            # print(a)
            # print(a.get('title'))
            titles.append(a.get('title'))
            urls.append('https://pib.gov.in/'+a.get('href'))


# In[49]:


text_data = []
i=0
for url in urls:
    html_content = get(url,headers=headers)
    soup = BeautifulSoup(html_content.text, 'html.parser')
    text = soup.find_all('p',style="text-align:justify")

    concat_text = ''
    for t in text:
        # print(t)
        
        concat_text += t.text
    text_data.append([concat_text])


# In[50]:


df2 = pd.DataFrame({'Headings':titles, 'Link':urls,'text_data':text_data})


# In[51]:


df2.text_data = df2.text_data.apply(extract)


# In[52]:


df2


# In[53]:


df2['text_data'].replace('', np.nan, inplace=True)


# In[54]:


df2.dropna(axis=0, subset=['text_data'], thresh=1, inplace=True)


# In[55]:


df2


# In[56]:


df2['char_count']=df2['text_data'].str.len()


# In[57]:


df2


# In[58]:


df2 = df2[df2['char_count'] > 100]


# In[59]:


from langdetect import detect, DetectorFactory


# In[60]:


# Set seed for consistent results
DetectorFactory.seed = 0


# In[61]:


def is_english(text):
    try:
        return detect(text) == 'en'
    except:
        return False


# In[62]:


# Apply the function to the DataFrame
df2['is_english'] = df2['text_data'].apply(is_english)


# In[63]:


df2


# In[64]:


df2_final = df2[df2['is_english'] == True]


# In[65]:


df2_final.drop(columns=['is_english','char_count'],axis=1,inplace=True)


# In[66]:


# df2.to_csv('PIB.csv', mode='w',index=False,encoding='utf-8-sig')
df2_final.to_csv('PIB.csv', mode='w',index=False,encoding='utf-8')


# In[67]:


df2_final


# ## Federal Reserve

# In[68]:


html_content = get('https://www.federalreserve.gov/',headers=headers)


# In[69]:


soup = BeautifulSoup(html_content.text, 'html.parser')


# In[70]:


target_div = soup.find('div', {'class': 'col-xs-12 col-sm-8'})


# In[71]:


# Find all the list items within the target div
list_items = target_div.find_all('li')


# In[72]:


# Create empty lists to store headings and URLs
headings = []
urls = []

# Extract the heading and URL from each list item
for item in list_items:
    # Find the link within the list item
    link = item.find('a')
    if link:
        # Extract the heading and URL
        heading = link.text.strip()
        url = 'https://www.federalreserve.gov/' + link.get('href')
        headings.append(heading)
        urls.append(url)
        print(f'Heading: {heading}')
        print(f'URL: {url}')
        print()


# In[73]:


data = {'Headings':headings,'Link':urls}


# In[74]:


df4 = pd.DataFrame(data)


# In[75]:


df4['text_data']=np.nan
df4['Summary']=np.nan
df4['Gist']=np.nan


# In[76]:


df4


# In[77]:


df4.to_csv('USA.csv', mode='w',index=False,encoding='utf-8')


# In[ ]:




