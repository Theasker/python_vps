from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from telegramBot.telegramBot import TelegramBot
from youtube.youtubeAPI import YoutubeAPI
from datetime import datetime
import http.client

app = FastAPI()
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

"""
# Telegram webhook
from fastapi import FastAPI, Request
import telegram

app = FastAPI()
bot_token = "YOUR_BOT_TOKEN"
bot = telegram.Bot(token=bot_token)

@app.post("/telegram_webhook")
async def telegram_webhook(request: Request):
    update = telegram.Update.de_json(await request.json(), bot)
    chat_id = update.message.chat.id
    message_text = update.message.text
    bot.send_message(chat_id=chat_id, text=f"Received message: {message_text}")

    return {"ok": True}
"""