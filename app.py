
import streamlit as st
import asyncio
import edge_tts
import tempfile
import os
from deep_translator import GoogleTranslator

st.set_page_config(page_title="Voice App", page_icon="🎙️")

st.title("🎙️ My Voice App")
st.write("Type text and hear it speak!")

text = st.text_area("Enter text:", "Hello, welcome to my voice app!")

lang = st.selectbox("Choose language:", ["en", "fr", "es", "ig", "yo", "ha"])
voice_map = {
    "en": "en-US-JennyNeural",
    "fr": "fr-FR-DeniseNeural", 
    "es": "es-ES-ElviraNeural",
    "ig": "en-NG-EzinneNeural",
    "yo": "en-NG-EzinneNeural",
    "ha": "en-NG-EzinneNeural"
}

async def generate_speech(text, voice):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(tmp.name)
    return tmp.name

if st.button("🔊 Generate Voice"):
    if text.strip() == "":
        st.warning("Please enter text")
    else:
        with st.spinner("Generating..."):
            # Translate if not English
            if lang != "en":
                try:
                    text = GoogleTranslator(source='auto', target=lang).translate(text)
                except:
                    pass
            
            voice = voice_map.get(lang, "en-US-JennyNeural")
            file_path = asyncio.run(generate_speech(text, voice))
            
            st.audio(file_path, format="audio/mp3")
            st.success("Done! You can play and download")
            
            with open(file_path, "rb") as f:
                st.download_button("Download MP3", f, file_name="voice.mp3")
