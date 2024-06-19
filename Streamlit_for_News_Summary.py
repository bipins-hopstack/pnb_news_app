#!/usr/bin/env python
# coding: utf-8

# In[92]:


import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from PIL import Image


# In[93]:

url1 = 'https://github.com/bipins-hopstack/pnb_news_app/blob/main/RBI_18JUN.csv?raw=true'
df1 = pd.read_csv(url1)



# In[94]:

url2='https://github.com/bipins-hopstack/pnb_news_app/blob/main/SEBI_PFRDA.xlsx?raw=true'
df2 = pd.read_excel(url2)


# In[95]:


consolidated_1 = '''\n- RBI will conduct a Variable Rate Repo (VRR) auction on June 18, 2024, with the same guidelines as outlined in Press Release 2021-2022/1572 dated January 20, 2022.\n- Purvanchal Co-operative Bank in Uttar Pradesh has had its license cancelled by RBI due to insufficient capital and poor earning prospects. Depositors are entitled to insurance claim amounts up to ₹5 lakh from the Deposit Insurance and Credit Guarantee Corporation.\n- Premature redemption of Sovereign Gold Bonds issued in December 2017 will be allowed from June 18, 2024, after five years from the date of issue. The redemption price will be based on the simple average of the closing gold price of the previous three business days before the date of redemption.\n- RBI will sell two dated securities worth ₹23,000 crore through auction using the multiple price method. Both competitive and non-competitive bids are accepted, and interest on the securities will generally be paid half-yearly.\n- RBI has fined Sonali Bank PLC ₹96.40 lakh for violating the Credit Information Companies (Regulation) Act, 2005 and not complying with the Know Your Customer (KYC) directions and SWIFT-related operational controls.\n- RBI has fined Central Bank of India ₹1.45 crore for violating regulatory directions related to loans and customer protection.'''


# In[96]:


consolidated_2 = '''\n- SEBI has launched a free, voluntary online certification program in collaboration with NISM to help investors test their knowledge of markets and investing. The certification aims to assist individuals in gaining comprehensive knowledge about investing in the Indian securities markets.\n- SEBI has updated the "Saaṛthi2.0" mobile app, featuring a user-friendly interface, financial calculators, modules on KYC procedures, mutual funds, buying and selling shares, investor grievances redressal mechanism, and the Online Dispute Resolution (ODR) platform.\n- IRDAI has simplified the regulatory framework for the insurance sector, consolidating 37 regulations into 7 and introducing two new regulations, effective from April 1, 2024. IRDAI has also issued a Master Circular on Life Insurance business, consolidating provisions from four existing circulars, introducing a Customer Information Sheet, mandatory policy loans, health riders, partial withdrawals, and a longer free look period. The move aims to simplify and enhance transparency in life insurance, making it easier for policyholders to understand and make informed decisions'''


# In[97]:


# To get one day ago details

# current_datetime = datetime.now() - timedelta(days=1)
# formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

# Get current date and time
#current_datetime = datetime.now().strftime("%Y-%m-%d")


# In[98]:


def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo


# In[99]:


# Function to display dataframe with text wrap and hyperlinks
def display_dataframe(df):
    for i, row in df.iterrows():
        st.markdown(f"•  **{row['Headings']}**")
        st.markdown(f"[Click Here to access News URL]({row['Link']})")


# In[100]:


# Streamlit UI
st.title("News Dashboard")

# Sidebar with collapsible section for RBI News
st.sidebar.image(add_logo(logo_path="https://github.com/bipins-hopstack/pnb_news_app/blob/main/PNBLogo.png?raw=true", width=175, height=85), use_column_width=True)
st.sidebar.markdown('## RBI SEBI IRDAI News 14th June to 18th June 2024')

# Radio button to select the news category
news_category = st.sidebar.radio(
    "Select News Category",
    ('RBI News', 'SEBI & IRDAI News')
)

# Options for displaying news
news_option = None
if news_category == 'RBI News':
    news_option = st.sidebar.radio(
        "Select News Option",
        ('Gist of the News', 'News Headings with Summary', 'News Heading with URLs')
    )
elif news_category == 'SEBI & IRDAI News':
    news_option = st.sidebar.radio(
        "Select News Option",
        ('Gist of the News', 'News Headings with Summary', 'News Headings with URLs')
    )

# Display selected news based on category and option
if news_category == 'RBI News':
    if news_option == 'Gist of the News':
        st.header("Gist of the News")
        st.write(consolidated_1)
    elif news_option == 'News Headings with Summary':
        st.header("News Headings with Summary")
        for heading,summary in zip(df1['Headings'],df1['Summary']):
            st.markdown(f"•  **{heading}**")                       
            st.write(summary)
    elif news_option == 'News Heading with URLs':
        st.header("News Heading with URLs")
        display_dataframe(df1)
        
elif news_category == 'SEBI & IRDAI News':
    if news_option == 'Gist of the News':
        st.header("Gist of the News")
        st.write(consolidated_2)
    elif news_option == 'News Headings with Summary':
        st.header("News Headings with Summary")
        for heading,summary in zip(df2['Headings'],df2['Summary']):
            st.markdown(f"•  **{heading}**")
            st.write(summary)
    elif news_option == 'News Headings with URLs':
        st.header("News Headings with URLs")
        display_dataframe(df2)


# In[ ]:





# In[ ]:




