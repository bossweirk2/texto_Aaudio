import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Conversor de Voz", page_icon="🎙️", layout="centered")

# --- TÍTULO E IMAGEN ---
st.markdown(
    """
    <h1 style="text-align:center; color:#1E3A8A;">🎵 Conversión de Texto a Audio</h1>
    """,
    unsafe_allow_html=True,
)
image_url = "282px-Captain_toad_powerstar.png"
st.image(image_url, width=350)

with st.sidebar:
    st.subheader("🗣️ Escribe un texto para escucharlo en voz alta")
    st.markdown("---")

# --- CREAR CARPETA TEMPORAL ---
os.makedirs("temp", exist_ok=True)

# --- TEXTO DE HISTORIA INFANTIL ---
st.subheader("📖 Pequeña historia infantil")
st.write(
    "Había una vez una estrella que no quería dormir. "
    "Cada noche brillaba más fuerte para saludar a los niños del mundo. "
    "Pero un día, una nube traviesa la abrazó, y la estrella aprendió que descansar también la hacía brillar más."
)

# --- ÁREA DE TEXTO ---
st.markdown("¿Quieres escuchar otra historia? Escribe tu propio texto 👇")
text = st.text_area("Texto a convertir en audio:", height=150)

# --- SELECCIÓN DE IDIOMA ---
option_lang = st.selectbox("Selecciona el idioma:", ("Español", "English"))
lg = "es" if option_lang == "Español" else "en"

# --- BOTÓN DE CONVERSIÓN ---
def text_to_speech(text, lang):
    tts = gTTS(text, lang=lang)
    filename = "temp/audio.mp3"
    tts.save(filename)
    return filename

if st.button("🎧 Convertir a Audio"):
    if text.strip() == "":
        st.warning("Por favor, escribe un texto antes de convertirlo.")
    else:
        audio_path = text_to_speech(text, lg)
        audio_file = open(audio_path, "rb")
        audio_bytes = audio_file.read()

        st.markdown("## 🔊 Tu audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        # --- BOTÓN DE DESCARGA ---
        with open(audio_path, "rb") as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="voz_santiago.mp3">📥 Descargar Audio</a>'
        st.markdown(href, unsafe_allow_html=True)

# --- LIMPIEZA AUTOMÁTICA ---
def remove_files(n):
    mp3_files = glob.glob("temp/*.mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

remove_files(7)

# --- PIE DE PÁGINA ---
st.markdown(
    """
    <hr>
    <p style="text-align:center; color:#2563EB;">
    Hecho por <b>Santiago Velásquez</b>
    </p>
    """,
    unsafe_allow_html=True,
)
