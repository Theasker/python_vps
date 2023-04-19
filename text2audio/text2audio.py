# Requirements: apk add espeak espeak-dev py3-pyaudio
# https://ulife.ai/stories/top-free-text-to-speech-tts-libraries-for-python

import pyttsx3
from gtts import gTTS
import sys, os
sys.path.append("..")
from telegramBot.telegramBot import TelegramBot

filename = "audio.mp3"

def delete_file(filename):
    # Borro el fichero si exite   
    if os.path.exists(filename):
        print(f"fichero {filename} existe. Borrando...")
        os.remove(filename)

def save_text_to_audio_file(text):
    
    # Función para cambiar el idioma de lectura
    # language  : en_US, de_DE, ...
    # gender    : VoiceGenderFemale, VoiceGenderMale
    
    def change_voice(engine, language, gender='VoiceGenderFemale'):
        for voice in engine.getProperty('voices'):
            if language in voice.languages and gender == voice.gender:
                engine.setProperty('voice', voice.id)
                return True

        raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))
    
    # delete_file(filename)
    engine = pyttsx3.init()   
    # Configura la velocidad de lectura
    rate = engine.getProperty('rate')
    # print(f"rate: {rate}")
    engine.setProperty('rate', 200)
    
    # Configura el volumen
    #volume = engine.getProperty('volume')
    #engine.setProperty('volume', volume+0.50)
    
    # Configura el idioma
    
    #for voice in engine.getProperty('voices'):
    #    print(voice)

    voice = engine.getProperty('voice')
    #print(f"voice: {voice}")
    
    engine.setProperty('voice', 'spanish')
    # Configura las voces (voices[0] = masculina, voices[1] = femenina.)
    #voices = engine.getProperty('voices')
    # print(f"voices: {voices}")
    #engine.setProperty('voice', voices[0].id)    
    # Genera la salida de audio
    engine.save_to_file(text, "audio.mp3")
    engine.runAndWait()

def gtts(text):
    print("hola que tal")
    delete_file(filename)
    # Definir el texto a convertir en audio
    # texto = "Hola, este es un ejemplo de cómo convertir texto a voz en Python."

    # Crear un objeto gTTS con el texto y el idioma
    tts = gTTS(text, lang='es', slow=False)

    # Guardar el archivo de audio como un archivo mp3
    tts.save("audio.mp3")
    bot = TelegramBot("6181016891:AAFY_fpL6DoWm4pZ3LVxosq9wCAEzILFA0Y")
    print(bot.send_media(filename, "audio"))

""" bot = TelegramBot("6181016891:AAFY_fpL6DoWm4pZ3LVxosq9wCAEzILFA0Y")

texto = "Hola, este es un ejemplo de cómo convertir texto a voz en Python."
save_text_to_audio_file(texto)
bot.send_media(filename, "audio")
delete_file(filename) """

""" 
filename = "gtts.mp3"
gtts(texto, filename)
bot.send_media(filename, "audio")
delete_file(filename)
 """