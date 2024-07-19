import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from PIL import Image
from gtts import gTTS
import base64
from io import BytesIO
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
import unicodedata
import requests
from io import StringIO


def read_github_csv(url):
    # List of encodings to try
    encodings = ['utf-8', 'ISO-8859-1', 'latin1', 'cp1252']
    
    # First, get the raw content
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the file. Status code: {response.status_code}")

    content = response.content

    # Try different encodings
    for encoding in encodings:
        try:
            # Try to decode and read as CSV
            decoded_content = content.decode(encoding)
            df = pd.read_csv(StringIO(decoded_content))
            print(f"Successfully read with encoding: {encoding}")
            return df
        except UnicodeDecodeError:
            print(f"Failed with encoding: {encoding}")
            continue
        except pd.errors.ParserError:
            print(f"Parser error with encoding: {encoding}")
            continue

    # If all attempts fail, try with 'replace' error handling
    try:
        decoded_content = content.decode('utf-8', errors='replace')
        df = pd.read_csv(StringIO(decoded_content))
        print("Read with 'replace' error handling")
        return df
    except Exception as e:
        print(f"All reading attempts failed. Error: {str(e)}")
        return None

def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo
    
# AIwithSS commenting out the function as Links included in summary

def display_dataframe(df):
    for i, row in df.iterrows():
        st.markdown(f"•  **{row['Headings']}**")
        st.markdown(f"[Click Here to access News URL]({row['Link']})")


def clean_text(text):
        # Remove any non-printable characters
    return ''.join(ch for ch in text if unicodedata.category(ch)[0] != 'C')

def create_category_content(df, category_name):
    content = []
    border_color = colors.HexColor("#A20E37")
    styles = getSampleStyleSheet()
    
    # Header
    header_style = ParagraphStyle('Header', alignment=TA_CENTER, textColor=border_color)
    header = Paragraph("Document Header", header_style)
    content.append(header)
    content.append(Spacer(1, 20))
    
    # Category Title
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], alignment=TA_CENTER, textColor=border_color)
    content.append(Paragraph(clean_text(category_name), title_style))
    content.append(Spacer(1, 20))
    
    # Content with border
    data = []
    for _, row in df.iterrows():
        try:
            # Article Heading
            heading_style = ParagraphStyle('Heading2', parent=styles['Heading2'], textColor=border_color)
            data.append([Paragraph(clean_text(row['Headings']), heading_style)])
            data.append([Spacer(1, 10)])
            
            # Article Summary
            data.append([Paragraph(clean_text(row['Summary']), styles['Normal'])])
            data.append([Spacer(1, 20)])
        except Exception as e:
            print(f"Error processing row: {e}")
            continue  # Skip this row and continue with the next
    
    # Create a table with a border
    table = Table(data, colWidths=[7*inch])  # Adjust the width as needed
    table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    content.append(table)
    
    # Footer
    content.append(Spacer(1, 20))
    footer_style = ParagraphStyle('Footer', alignment=TA_CENTER, textColor=border_color)
    footer = Paragraph("Page Footer", footer_style)
    content.append(footer)
    
    content.append(PageBreak())
    return content

def generate_full_pdf(buffer,df1, df2, df3):
    
    doc = SimpleDocTemplate(buffer)
    story = []
    try:
        story.extend(create_category_content(df1, "RBI News"))
        story.extend(create_category_content(df2, "SEBI & IRDAI News"))
        story.extend(create_category_content(df3, "PIB News"))
        doc.build(story)
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None  # Return None if PDF generation fails

    
def text_to_speech(text, key):
    if key not in st.session_state.audio_data:
        tts = gTTS(text=text, lang='en')
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        audio_bytes = mp3_fp.read()
        b64 = base64.b64encode(audio_bytes).decode()
        st.session_state.audio_data[key] = b64
    else:
        b64 = st.session_state.audio_data[key]
        
        html_string = f"""
            <audio id="audio-{key}" style="display:none">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            <button id="play-{key}" onclick="playAudio('{key}')">Play</button>
            <button id="stop-{key}" onclick="stopAudio('{key}')" style="display:none">Stop</button>
            <script>
                var audio_{key} = document.getElementById("audio-{key}");
                var playBtn_{key} = document.getElementById("play-{key}");
                var stopBtn_{key} = document.getElementById("stop-{key}");
        
                function playAudio(key) {{
                    audio_{key}.play();
                    playBtn_{key}.style.display = "none";
                    stopBtn_{key}.style.display = "inline-block";
                }}
        
                function stopAudio(key) {{
                    audio_{key}.pause();
                    audio_{key}.currentTime = 0;
                    playBtn_{key}.style.display = "inline-block";
                    stopBtn_{key}.style.display = "none";
                }}
        
                audio_{key}.onended = function() {{
                    stopAudio('{key}');
                }};
            </script>
        """
        st.components.v1.html(html_string, height=50)

# Initialize session state
if 'audio_data' not in st.session_state:
    st.session_state.audio_data = {}
# Import existing dataframes
url1 = "https://github.com/bipins-hopstack/pnb_news_app/blob/main/RBI.csv?raw=true"
url2 = "https://github.com/bipins-hopstack/pnb_news_app/blob/main/SEBI_PFRDA_21JUN.csv?raw=true"
url3 = "https://github.com/bipins-hopstack/pnb_news_app/blob/main/PIB.csv?raw=true"
url4 = "https://github.com/bipins-hopstack/pnb_news_app/blob/main/RBI_NOTIFICATION.csv?raw=true"
url5 = "https://github.com/bipins-hopstack/pnb_news_app/blob/main/USA.csv?raw=true"
url6 = "https://github.com/bipins-hopstack/pnb_news_app/blob/main/Japan.csv?raw=true"

df1 = read_github_csv(url1)
df2 = read_github_csv(url2)
df3 = read_github_csv(url3)
df4 = read_github_csv(url4)
df5 = read_github_csv(url5)
df6 = read_github_csv(url6)

rbi_gist = df1.iloc[0]['Gist']
sebi_gist = df2.iloc[0]['Gist']
pib_gist = df3.iloc[0]['Gist']


# Streamlit UI
st.title("News Dashboard")

# Sidebar with collapsible section for RBI News
st.sidebar.image(add_logo(logo_path="PNBLogo.png", width=175, height=85), use_column_width=True)
st.sidebar.markdown('## NEWS - RBI/PIB <span style="font-size: medium">Latest</span>', unsafe_allow_html=True)

# Radio button to select the news category
news_category = st.sidebar.radio(
    "Select News Category",
    ('RBI News', 'PIB News', 'RBI Notification','Federal Central Bank','Bank of Japan')
)

# Options for displaying news
news_option = None
if news_category == 'RBI News':
    news_option = st.sidebar.radio(
        "Select News Option",
        ('Gist of the News', 'News Headings with Summary')
    )
#elif news_category == 'SEBI & IRDAI News':
    #news_option = st.sidebar.radio(
        #"Select News Option",
        #('Gist of the News', 'News Headings with Summary')
    #)
elif news_category == 'PIB News':
    news_option = st.sidebar.radio(
        "Select News Option",
        ('Gist of the News', 'News Headings with Summary')
    )
elif news_category == 'RBI Notification':
    display_dataframe(df4)
elif news_category == 'Federal Central Bank':
    display_dataframe(df5)
elif news_category == 'Bank of Japan':
    display_dataframe(df6)
    
    

# Display selected news based on category and option
# AIwithSS - modified loop to diplay link under Summaries

if news_category == 'RBI News':
    if news_option == 'Gist of the News':
        st.header("Gist of the News")
        text_to_speech(rbi_gist, "rbi_gist")
        st.write(rbi_gist)
    elif news_option == 'News Headings with Summary':
        st.header("News Headings with Summary")
        for i, (heading, summary, link) in enumerate(zip(df1['Headings'], df1['Summary'],df1['Link'])):
            st.markdown(f"•  **{heading}**")
            text_to_speech(summary, f"rbi_{i}")
            st.write(summary)
            st.markdown(f"[Click Here to access News URL]({link})")
            st.markdown("---")
    #elif news_option == 'News Heading with URLs':
        #st.header("News Heading with URLs")
        #display_dataframe(df1)
        
#elif news_category == 'SEBI & IRDAI News':
    #if news_option == 'Gist of the News':
        #st.header("Gist of the News")
        #text_to_speech(sebi_gist, "sebi_gist")
        #st.write(sebi_gist)
    #elif news_option == 'News Headings with Summary':
        #st.header("News Headings with Summary")
        #for i, (heading, summary,link) in enumerate(zip(df2['Headings'], df2['Summary'],df2['Link'])):
            #st.markdown(f"•  **{heading}**")
            #text_to_speech(summary, f"sebi_{i}")
            #st.write(summary)
            #st.markdown(f"[Click Here to access News URL]({link})")
            #st.markdown("---")
      
        
    #elif news_option == 'News Headings with URLs':
        #st.header("News Headings with URLs")
        #display_dataframe(df2)
        
elif news_category == 'PIB News':
    if news_option == 'Gist of the News':
        st.header("Gist of the News")
        text_to_speech(pib_gist, "pib_gist")
        st.write(pib_gist)
    elif news_option == 'News Headings with Summary':
        st.header("News Headings with Summary")
        for i, (heading, summary,link) in enumerate(zip(df3['Headings'], df3['Summary'],df3['Link'])):
            st.markdown(f"•  **{heading}**")
            text_to_speech(summary, f"pib_{i}")
            st.write(summary)
            st.markdown(f"[Click Here to access News URL]({link})")
            st.markdown("---")
   # elif news_option == 'News Headings with URLs':
   #     st.header("News Headings with URLs")
   #     display_dataframe(df3)


    


# Add this to your Streamlit app's sidebar
if st.sidebar.button('Download Full Report'):
    buffer = BytesIO()
    pdf = generate_full_pdf(buffer, df1, df2, df3)
    if pdf:
        st.sidebar.download_button(
            label="Click here to download the PDF",
            data=pdf,
            file_name="full_news_report.pdf",
            mime="application/pdf"
        )
    else:
        st.sidebar.error("Failed to generate PDF. Please try again.")
