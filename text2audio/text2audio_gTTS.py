from gtts import gTTS
import os

# Definir el texto a convertir en audio
texto = "Hola, este es un ejemplo de cómo convertir texto a voz en Python."

# Crear un objeto gTTS con el texto y el idioma
tts = gTTS(texto, lang='es', slow=False)

# Guardar el archivo de audio como un archivo mp3
tts.save("audio.mp3")
