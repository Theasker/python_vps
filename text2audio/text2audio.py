# Requirements: apk add espeak espeak-dev py3-pyaudio

import pyttsx3
from pydub import AudioSegment
from pydub.utils import make_chunks
import sys, os
sys.path.append("..")
from telegramBot.telegramBot import TelegramBot

def save_text_to_audio_file(text, filename, format='mp3', bitrate='192k'):
    engine = pyttsx3.init()
    
    # Configura la velocidad de lectura
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 350)  
    # Configura el volumen
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume+0.50)
    # Configura el idioma
    voice = engine.getProperty('voice')
    engine.setProperty('voice', 'spanish')
    # Configura las voces (voices[0] = masculina, voices[1] = femenina.)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    # Genera la salida de audio
    engine.save_to_file(text, filename)
    engine.runAndWait()
    

save_text_to_audio_file("Erase una vez un lobo", "temp.mp3")
bot = TelegramBot("6181016891:AAFY_fpL6DoWm4pZ3LVxosq9wCAEzILFA0Y")
# send_media(self, filename, type, caption="", chat_id = '-797062014' ):
bot.send_media("temp.mp3", "audio")
os.remove("/usr/src/app/text2audio/temp.mp3")