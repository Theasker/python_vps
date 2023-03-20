from fastapi import FastAPI, Request
from telegramBot.telegramBot import TelegramBot
from datetime import datetime
import http.client

app = FastAPI()

@app.get("/")
def root():
    #return {"message": "Hello World"}
    return f"Hola mundo a las {datetime.now()}"

@app.get("/spotify/{item_id}")
def read_item(item_id: str):
    conn = http.client.HTTPSConnection('eolmlyay4to9iia.m.pipedream.net')
    conn.request("POST", "/", '{"test": "hola"}', {'Content-Type': 'application/json'})
    
    return {
        "spotify": item_id,
        "time": datetime.now()
        }

"""
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