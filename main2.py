import configparser
import logging
import json
import requests
# import inspect
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from datetime import datetime
#import http.client
#from telegramBot.telegramBot import TelegramBot
# from youtube.youtubeAPI import YoutubeAPI
# from utils.utils import Utils

# Carga de las variables de configuración
config = configparser.ConfigParser() 
config.read('/usr/src/app/config.ini')
bot_token = config['TELEGRAM']['BOT_TOKEN']
url_base = config['TELEGRAM']['URL_BASE']
# Configuración del logger
logging.basicConfig(
    filename='main.log', 
    encoding='utf-8', 
    level=logging.INFO,
    format='%(asctime)s:  %(name)s: %(levelname)s: %(message)s', 
    datefmt='%Y/%m/%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

#bot = TelegramBot(bot_token)

app = FastAPI()

# La URL de la API de Telegram
URL = f"https://api.telegram.org/bot{bot_token}"

#print(f"Ejecutando línea: {inspect.currentframe().f_lineno}")

def prettyJson(json):
    json_object = json.loads(json_data)
    return json.dumps(json_object, indent=2)

@app.post("/telegram")
async def telegram_webhook(request: Request):
    #logger.info("Dentro de la ruta \"/telegram\"")
    # Obtener el cuerpo del mensaje recibido
    body = await request.body()
    """
    # Convertir el cuerpo a un objeto Python
    update = json.loads(body.decode("utf-8"))
    # Obtener los datos del mensaje recibido
    message = update["message"]
    chat_id = message["chat"]["id"]
    text = message["text"]
    # Realizar alguna acción en respuesta al mensaje
    response_text = f"Recibido mensaje: {text}"
    # Enviar una respuesta al usuario
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, json=payload)
    """
    print(body)
    return {"ok": True}

 
@app.get("/")
def root():
    return {"message": datetime.now()}


@app.get("/", response_class=HTMLResponse)
async def read_items():

    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>{datetime.now()}</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/spotify/{item_id}")
def read_item(item_id: str):
    # pipedream ##############################################
    conn = http.client.HTTPSConnection('eolmlyay4to9iia.m.pipedream.net')
    conn.request("POST", "/", '{"test": "hola"}', {'Content-Type': 'application/json'})
    # pipedream END ##########################################
    
    return {
        "spotify": item_id,
        "time": datetime.now()
        }

@app.get("/youtube")
async def youtube():
    yt = YoutubeAPI()
    # return yt._get_videos_from_channel("atareao")
    return {"user_id": "the current user"}


if __name__ == "__main__":
    out = bot.get_WebhookInfo(bot_token)
    print(out)
