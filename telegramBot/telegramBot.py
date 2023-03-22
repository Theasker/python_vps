#!/usr/bin/python3
#-*- coding: utf-8 -*-

# config.ini structure
#
# {
#     "token": "xxxx:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
#     "channel": "-1111111111111",
#     "group": "-22222222222",
#     "botname": "name_bot",
#     "url": "https://api.telegram.org/bot",
#     "url_local": "http://172.22.0.2:8081/bot"
# }

import requests, json, sys, os
from datetime import datetime
from os.path import exists

PROPERTIES = '/usr/src/app/telegramBot/config.json'

class TelegramBot():

    # Pasamos como parámetro el token del bot al instanciar
    def __init__(self, botToken):
        self._params = {} # Creo un diccionario para las variables del fichero
        self._url = None
        self.get_properties(botToken)
        # print(self._params)
        # self.dispatch()

    def get_properties(self, botToken):
        properties = []
        try:
            with open(PROPERTIES, 'r') as file:
                self._params = json.load(file)
                self._params['token'] = botToken
                self._url = f"{self._params['url_local']}{self._params['token']}/"
        except OSError:
            print("Could not open/read file:", fname)
            sys.exit()

    def set_webhook(self, url):
        set_webhook_url = self._url + f"setWebhook?url={url}"
        response = requests.get(set_webhook_url)
        if response.status_code == 200:
            return "Webhook has been set successfully."
        else:
            return f"Error setting webhook: {response.content.decode('utf-8')}"

    def get_WebhookInfo(self, botToken):
        url = f"{self._url}getWebhookInfo"
        response = requests.get(url)
        return response.content

    def get_me(self):
        method = "getme"
        url = self._url + "/" + method
        response = requests.get(url + method)
        #response = requests.get(self._url + method)
        return json.loads(response.text)

    def get_updates(self):
        # Last updates of the bot in the groups, channels, etc
        method = "getupdates"
        response = requests.get(self._url + method)
        if response.status_code == 200:
            # Convertimos la salida json en un objeto
            output = json.loads(response.text)
            return output
        return None

    def send_message(self, message, chat_id = '-797062014' ):
        method = "sendmessage"
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML',
            'disable_web_page_preview': True
            }
        response = requests.post(self._url + method, data=data)
        return json.loads(response.text)

    def send_media(self, filename, type, caption="", chat_id = '-797062014' ):
        # try open the file for check if exists
        try:
            file = open(filename, 'rb')
            data = {
                    'chat_id': chat_id,
                    'caption': caption
                    }
            if (type == "photo"):
                method = "sendPhoto"
                files = {'photo': file}    
            elif (type == "audio"):
                method = "sendAudio"
                files = {'audio': file}    
            elif (type == "video"):
                method = "sendVideo"
                files = {'video': file} 
            else:
                data = {
                    'chat_id': chat_id,
                    'caption': caption,
                    'disable_content_type_detection': False
                    }
                method = "sendDocument"
                files = {'document': file} 
            
            response = requests.post(self._url + method, data, files=files)
            return json.loads(response.text)
        except IOError as e:
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
        except: #handle other exceptions such as attribute errors
            print ("Unexpected error:", sys.exc_info()[0])

    # Chat Updates the last 24 hours  
    def get_updates_chat(self, chat_id = '-797062014'):
        method = "getupdates"
        data = {'chat_id': chat_id}
        response = requests.post(self._url + method, data)
        return json.loads(response.text)

    def send_path(self, path):
        count = 1
        for root, dir_names, file_names in os.walk(path):
            # print(f"The root is {root}")
            # print(f"The directory name is: {dir_names}")
            # print(f"The file names are: {file_names}")
            # print(f"{root}")
            for file in file_names:
                filepath = root + "/" + file
                response = self.send_media(self._params['channel'], filepath, "document", file)
                if response['ok']:
                    print(count, "-", filepath, "✔")
                count = count + 1

    def dispatch(self):
        print (sys.argv)
        print (len(sys.argv))
        # check number arguments
        if len(sys.argv) > 1 & len(sys.argv) <= 5: 
            if sys.argv[1] == "-m":
                if 2 >= len(sys.argv):
                    self.help()
                else:
                    response = self.send_message(sys.argv[2])
                    if response['ok']:
                        print("message sent!")
            elif sys.argv[1] == "-h":
                self.help()
            elif sys.argv[1] == "-i":
                if (len(sys.argv) == 4): # Check caption option
                    response = self.send_media(self._params['channel'],sys.argv[2],"photo",sys.argv[3])
                else: 
                    response = self.send_media(self._params['channel'],sys.argv[2],"photo")
                if(response['ok']):
                    print("Image sent!")
            elif sys.argv[1] == "-a":
                if (len(sys.argv) == 5): # Check parameters number
                    # Verifico que el fichero existe
                    if os.path.exists(sys.argv[2]):
                        response = self.send_media(sys.argv[2],"audio",sys.argv[3],sys.argv[4])
                        if(response['ok']):
                            print("Audio sent!")
                    # El fichero de audio no existe
                    else:
                        print ('El fichero' + sys.argv[2] + 'no existe')
                elif (len(sys.argv) == 4): # Check caption option
                    # Verifico que el fichero existe
                    if os.path.exists(sys.argv[2]):
                        response = self.send_media(sys.argv[2],"audio",sys.argv[3])
                        if(response['ok']):
                            print("Audio sent!")
                    # El fichero de audio no existe
                    else:
                        print ('El fichero' + sys.argv[2] + 'no existe')
                elif (len(sys.argv) == 3):
                    if os.path.exists(sys.argv[2]):
                        response = self.send_media(sys.argv[2],"audio")
                        if(response['ok']):
                            print("Audio sent!")
                    # El fichero de audio no existe
                    else:
                        print ('El fichero "' + sys.argv[2] + '" no existe')       
                else: 
                    self.help()
            elif sys.argv[1] == "-v":
                if (len(sys.argv) == 5): # Check parameters number
                    # Verifico que el fichero existe
                    if os.path.exists(sys.argv[2]):
                        response = self.send_media(sys.argv[2],"video",sys.argv[3],sys.argv[4])
                        if(response['ok']):
                            print("Video sent!")
                    # El fichero de audio no existe
                    else:
                        print ('El fichero' + sys.argv[2] + 'no existe')
                elif (len(sys.argv) == 4): # Check caption option
                    # Verifico que el fichero existe
                    if os.path.exists(sys.argv[2]):
                        response = self.send_media(sys.argv[2],"video",sys.argv[3])
                        if(response['ok']):
                            print("Video sent!")
                    # El fichero de audio no existe
                    else:
                        print ('El fichero' + sys.argv[2] + 'no existe')
                elif (len(sys.argv) == 3):
                    if os.path.exists(sys.argv[2]):
                        response = self.send_media(sys.argv[2],"video")
                        if(response['ok']):
                            print("Video sent!")
                    # El fichero de audio no existe
                    else:
                        print ('El fichero "' + sys.argv[2] + '" no existe')       
                else: 
                    self.help()
            elif sys.argv[1] == "-d":
                if (len(sys.argv) == 5): # Check parameters number
                    # Verifico que el fichero existe
                    if os.path.exists(sys.argv[2]):
                        response = self.send_media(sys.argv[2],"audio",sys.argv[3],sys.argv[4])
                        if(response['ok']):
                            print("Audio sent!")
                    # El fichero de audio no existe
                    else:
                        print ('El fichero' + sys.argv[2] + 'no existe')
                elif (len(sys.argv) == 4): # Check caption option
                    # Verifico que el fichero existe
                    if os.path.exists(sys.argv[2]):
                        response = self.send_media(sys.argv[2],"document",sys.argv[3])
                        if(response['ok']):
                            print("Document sent!")
                    # El fichero de audio no existe
                    else:
                        print ('El fichero' + sys.argv[2] + 'no existe')
                elif (len(sys.argv) == 3):
                    if os.path.exists(sys.argv[2]):
                        response = self.send_media(sys.argv[2],"document")
                        if(response['ok']):
                            print("Document sent!")
                    # El fichero de audio no existe
                    else:
                        print ('El fichero "' + sys.argv[2] + '" no existe')       
                else: 
                    self.help()
            elif sys.argv[1] == "-p":
                if len(sys.argv) > 2:
                    self.send_path(sys.argv[2])
                else:
                    print("I need the path")
            elif sys.argv[1] == "--getupdates":
                response = self.get_updates()
                print(json.dumps(response, indent=2))
            else:
                self.help()
        # El número de parámetros no es el correcto
        else:
            print("El número de parámetros no es el correcto: " , len(sys.argv))
            self.help()
    
    def help(self):
        print(f"Usage: {os.path.basename(__file__)} [OPTION] [IMAGE | FILE | AUDIO | VIDEO | DOCUMENT] [Caption] [Group / Channel id]")
        print("\t-m <message>\t\t\tSend message")
        print("\t-h\t\t\t\tHelp options")
        print("\t-i <image path> [caption]\tSend a image")
        print("\t-a <audio path> [caption]\tSend a audio")
        print("\t-v <video path> [caption]\tSend a video")
        print("\t-d <document path> [caption]\tSend a document")
        print("\t-p <directory path> \t\tSends all files in the given directory and subdirectories.")
        print("\t--getupdates\t\t\tGet updates telegram method")

if __name__ == "__main__":
    telegram_bot = TelegramBot("5941895196:AAGBMQx-cTqgBXA4dzsyyZw_IViT8PWk3Dg")
    telegram_bot.send_message("hola que tal")
    # print(telegram_bot.get_updates())
    # Imprimo la última actualización
    # print(json.dumps(telegram_bot.get_updates()['result'][-1], indent=2))
    # print(telegram_bot.get_updates())
    #print(json.dumps(telegram_bot.get_updates(), indent=2))
    # now = datetime.now()
    # date_time = now.strftime("%Y/%m/%d, %H:%M:%S")
    # channelId: -1001519446927
    # groupId: -797062014
    # print(telegram_bot.send_message(date_time + " <b>Hola canal</b>","-1001519446927"))
    #print(telegram_bot.send_message(date_time + " <a href=\"https://laflordearagon.es\">laflordearagon</a>","-797062014"))
    #print(json.dumps(telegram_bot.get_updates_chat("-1001519446927"), indent=2))
