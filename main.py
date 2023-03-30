from fastapi import FastAPI, Request
import configparser
import logging
import json
from telegramBot.telegramBot import TelegramBot
from fastapi.responses import HTMLResponse
from datetime import datetime
from utils.utils import Utils

# import inspect

# Carga de las variables de configuración
config = configparser.ConfigParser() 
config.read('/usr/src/app/config.ini')
bot_token = config['TELEGRAM']['BOT_TOKEN']
url_base = config['TELEGRAM']['URL_BASE']
log_file = config['TELEGRAM']['LOG_FILE']
# Configuración del logger
logging.basicConfig(
    filename=log_file, 
    encoding='utf-8', 
    level=logging.INFO,
    format='%(asctime)s:  %(name)s: %(levelname)s: %(message)s', 
    datefmt='%Y/%m/%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

#print(f"Ejecutando línea: {inspect.currentframe().f_lineno}")

def truncate_file(file):
    try:
        with open(file, "r+") as f:
            f.truncate(0)
    except FileNotFoundError:
        print('El archivo no existe')
    except:
        print('Ocurrió un error')

app = FastAPI()

@app.post("/webhook")
async def telegram_webhook(request: Request):
    truncate_file(log_file)
    bot = TelegramBot(bot_token)
    data = await request.json()
    if (data["message"]):
        # Sacamos la información que necesito
        message = data["message"]
        chat_id = message["chat"]["id"]
        text = message["text"]
        name = message["from"]["first_name"]
        username = message["from"]["username"]
        logger.info(f"chat_id: {chat_id} / mensaje: {text} / name: {name} / username: {username}")
        logger.info(json.dumps(data, indent=2))
        if (text.startswith("/")):
            utils = Utils(text)
    return {"ok": True}

@app.get("/", response_class=HTMLResponse)
async def read_items():

    html_content = """
    <html>
        <head>
            <title>Python Telegram Bot</title>
        </head>
        <body>
            <h1>Python Telegram Bot</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

# Envía el parámetro de la url al bot de telegram
@app.get("/send/{message}/{chat_id}")
async def send_telegram(message: str, chat_id: str = None):
    bot = TelegramBot(bot_token)
    if chat_id:
        bot.send_message(message, chat_id)
        return {"time": datetime.now(), "message": message, "chat_id": chat_id}
    bot.send_message(message)
    return {"time": datetime.now(), "message": message}
 
@app.get("/date")
def root():
    return {"date": datetime.now()}

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
