import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from PIL import Image
from gtts import gTTS
import base64
from io import BytesIO

# Initialize session state
if 'audio_data' not in st.session_state:
    st.session_state.audio_data = {}

# Import existing dataframes
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

def display_dataframe(df):
    for i, row in df.iterrows():
        st.markdown(f"•  **{row['Headings']}**")
        st.markdown(f"[Click Here to access News URL]({row['Link']})")

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
        text_to_speech(rbi_gist, "rbi_gist")
        st.write(rbi_gist)
    elif news_option == 'News Headings with Summary':
        st.header("News Headings with Summary")
        for i, (heading, summary) in enumerate(zip(df1['Headings'], df1['Summary'])):
            st.markdown(f"•  **{heading}**")
            text_to_speech(summary, f"rbi_{i}")
            st.write(summary)
            st.markdown("---")
    elif news_option == 'News Heading with URLs':
        st.header("News Heading with URLs")
        display_dataframe(df1)
        
elif news_category == 'SEBI & IRDAI News':
    if news_option == 'Gist of the News':
        st.header("Gist of the News")
        text_to_speech(sebi_gist, "sebi_gist")
        st.write(sebi_gist)
    elif news_option == 'News Headings with Summary':
        st.header("News Headings with Summary")
        for i, (heading, summary) in enumerate(zip(df2['Headings'], df2['Summary'])):
            st.markdown(f"•  **{heading}**")
            text_to_speech(summary, f"sebi_{i}")
            st.write(summary)
            st.markdown("---")
    elif news_option == 'News Headings with URLs':
        st.header("News Headings with URLs")
        display_dataframe(df2)
        
elif news_category == 'PIB News':
    if news_option == 'Gist of the News':
        st.header("Gist of the News")
        text_to_speech(pib_gist, "pib_gist")
        st.write(pib_gist)
    elif news_option == 'News Headings with Summary':
        st.header("News Headings with Summary")
        for i, (heading, summary) in enumerate(zip(df3['Headings'], df3['Summary'])):
            st.markdown(f"•  **{heading}**")
            text_to_speech(summary, f"pib_{i}")
            st.write(summary)
            st.markdown("---")
    elif news_option == 'News Headings with URLs':
        st.header("News Headings with URLs")
        display_dataframe(df3)
