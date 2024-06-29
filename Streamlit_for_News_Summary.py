#!/usr/bin/env python
# coding: utf-8

# In[41]:


import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from PIL import Image

df1 = pd.read_csv("https://github.com/bipins-hopstack/pnb_news_app/blob/main/RBI.csv?raw=true")
df2 = pd.read_csv("https://github.com/bipins-hopstack/pnb_news_app/blob/main/SEBI_PFRDA_21JUN.csv?raw=true")
df3 = pd.read_csv("https://github.com/bipins-hopstack/pnb_news_app/blob/main/PIB.csv?raw=true")


rbi_gist = df1.iloc[0]['Gist']

sebi_gist = df2.iloc[0]['Gist']


pib_gist = df3.iloc[0]['Gist']



def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY


def generate_pdf(news_category, df):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    story = []

    # Add title
    title_style = styles['Heading1']
    title_style.textColor = colors.darkblue
    story.append(Paragraph(f"{news_category} News", title_style))
    story.append(Spacer(1, 12))

    # Add content
    for _, row in df.iterrows():
        heading_style = styles['Heading2']
        heading_style.textColor = colors.darkgreen
        story.append(Paragraph(row['Headings'], heading_style))
        story.append(Spacer(1, 6))
        
        story.append(Paragraph(row['Summary'], styles['Justify']))
        story.append(Spacer(1, 12))

    doc.build(story)
    buffer.seek(0)
    return buffer

# Add this to your Streamlit app
if st.button('Download PDF'):
    pdf = generate_pdf(news_category, df)
    st.download_button(
        label="Click here to download the PDF",
        data=pdf,
        file_name=f"{news_category}_news.pdf",
        mime="application/pdf"
    )




# Function to display dataframe with text wrap and hyperlinks
def display_dataframe(df):
    for i, row in df.iterrows():
        st.markdown(f"•  **{row['Headings']}**")
        st.markdown(f"[Click Here to access News URL]({row['Link']})")


# In[50]:


# Streamlit UI
st.title("News Dashboard")

# Sidebar with collapsible section for RBI News
st.sidebar.image(add_logo(logo_path="PNBLogo.png", width=175, height=85), use_column_width=True)
st.sidebar.markdown('## NEWS - RBI/SEBI/IRDAI/PIB <span style="font-size: medium">24th June 2024</span>', unsafe_allow_html=True)

# Radio button to select the news category
news_category = st.sidebar.radio(
    "Select News Category",
    ('RBI News', 'SEBI & IRDAI News','PIB News')
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
elif news_category == 'PIB News':
    news_option = st.sidebar.radio(
        "Select News Option",
        ('Gist of the News', 'News Headings with Summary', 'News Headings with URLs')
    )

# Display selected news based on category and option
if news_category == 'RBI News':
    if news_option == 'Gist of the News':
        st.header("Gist of the News")
        st.write(rbi_gist)
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
        st.write(sebi_gist)
    elif news_option == 'News Headings with Summary':
        st.header("News Headings with Summary")
        for heading,summary in zip(df2['Headings'],df2['Summary']):
            st.markdown(f"•  **{heading}**")
            st.write(summary)
    elif news_option == 'News Headings with URLs':
        st.header("News Headings with URLs")
        display_dataframe(df2)
        
elif news_category == 'PIB News':
    if news_option == 'Gist of the News':
        st.header("Gist of the News")
        st.write(pib_gist)
    elif news_option == 'News Headings with Summary':
        st.header("News Headings with Summary")
        for heading,summary in zip(df3['Headings'],df3['Summary']):
            st.markdown(f"•  **{heading}**")
            st.write(summary)
    elif news_option == 'News Headings with URLs':
        st.header("News Headings with URLs")
        display_dataframe(df3)


# In[ ]:





# In[ ]:




