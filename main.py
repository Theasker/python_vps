import configparser
import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from datetime import datetime
import http.client
from telegramBot.telegramBot import TelegramBot
from youtube.youtubeAPI import YoutubeAPI
from utils.utils import Utils

# Carga de las variables de configuración
config = configparser.ConfigParser() 
config.read('/usr/src/app/config.ini')
bot_token = config['TELEGRAM']['BOT_TOKEN']
url_base = config['TELEGRAM']['URL_BASE']
logging.basicConfig(
    filename='main.log', 
    encoding='utf-8', 
    level=logging.DEBUG,
    format='%(asctime)s:  %(name)s: %(levelname)s: %(message)s', 
    datefmt='%Y/%m/%d %H:%M:%S'
)
logger = logging.getLogger(__name__)
logger.info(option)

bot = TelegramBot(bot_token)

app = FastAPI()

def pipedream(text):
    conn = http.client.HTTPSConnection('eolmlyay4to9iia.m.pipedream.net')
    conn.request("POST", "/", f'{"test": "{text}"}', {'Content-Type': 'application/json'})

@app.post("/telegram")
async def telegram_webhook(request: Request):
    update = await request.json()
    chat_id = update["message"]["chat"]["id"]
    message_text = update["message"]["text"]
    pipedream(message_text)
    utils = Utils(message_text)
    utils.pruebas()
    return {"ok": True}

""" 
@app.get("/")
def root():
    return {"message": datetime.now()}
"""
@app.get("/", response_class=HTMLResponse)
async def read_items():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>FastAPI</h1>
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

# if __name__ == "__main__":
    