import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64
from pydub import AudioSegment

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Conversor de Voz", page_icon="🎙️", layout="centered")

# --- TÍTULO E IMAGEN ---
st.markdown(
    """
    <h1 style="text-align:center; color:#1E3A8A;">🎵 Conversión de Texto a Audio</h1>
    """,
    unsafe_allow_html=True,
)
image_url = "https://cdn.pixabay.com/photo/2017/06/20/19/22/child-2424026_1280.png"
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

# --- SLIDER DE TONO ---
st.markdown("### 🎚️ Ajusta el tono de la voz")
pitch_value = st.slider("Tono (pitch)", min_value=-5, max_value=5, value=0, step=1)

# --- FUNCIÓN PARA CONVERTIR TEXTO A AUDIO ---
def text_to_speech(text, lang):
    tts = gTTS(text, lang=lang)
    filename = "temp/audio.mp3"
    tts.save(filename)
    return filename

# --- AJUSTAR TONO ---
def adjust_pitch(file_path, semitones):
    sound = AudioSegment.from_file(file_path, format="mp3")
    new_sample_rate = int(sound.frame_rate * (2.0 ** (semitones / 12.0)))
    shifted = sound._spawn(sound.raw_data, overrides={"frame_rate": new_sample_rate})
    shifted = shifted.set_frame_rate(44100)
    shifted.export(file_path, format="mp3")

# --- BOTÓN DE CONVERSIÓN ---
if st.button("🎧 Convertir a Audio"):
    if text.strip() == "":
        st.warning("Por favor, escribe un texto antes de convertirlo.")
    else:
        audio_path = text_to_speech(text, lg)
        if pitch_value != 0:
            adjust_pitch(audio_path, pitch_value)

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
    Hecho con ❤️ por <b>Santiago Velásquez</b>
    </p>
    """,
    unsafe_allow_html=True,
)
