import logging
import subprocess
import json
import traceback
import configparser
import sys
# append the path of the parent directory
sys.path.append("..")
from telegramBot.telegramBot import TelegramBot
from text2audio.text2audio import save_text_to_audio_file, gtts

class Utils():
    def __init__(self, option):
        # Carga de las variables de configuración
        config = configparser.ConfigParser() 
        config.read('/usr/src/app/utils/config.ini')
        self.bot_token = config['UTILS']['BOT_TOKEN']
        self.url_base = config['UTILS']['URL_BASE']
        self.log_file = config['UTILS']['LOG_FILE']
        # Configuración del logger

        logger = logging.getLogger(__name__)
        logging.basicConfig(
            filename='utils.log', 
            encoding='utf-8', 
            level=logging.ERROR,
            format='%(asctime)s:  %(name)s: %(levelname)s: %(message)s', 
            datefmt='%Y/%m/%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(option)
        self.truncate_file(self.log_file)
        if (option.startswith("/")):
            self._dispatcher(option)
    
    def pipedream(self, text):
        conn = http.client.HTTPSConnection('eolmlyay4to9iia.m.pipedream.net')
        conn.request("POST", "/", f'"test": "{text}"', {'Content-Type': 'application/json'})

    def _dispatcher(self, option):
        if (option == '/wol'):
            self.wol()
        elif (option.startswith("/text2audio ")):
            gtts(option.replace("/text2audio ", ""))
        elif (option.startswith("/text2audio2 ")):
            save_text_to_audio_file(option.replace("/text2audio2 ", ""))
    
    def truncate_file(self,file):
        try:
            with open(file, "r+") as f:
                f.truncate(0)
        except FileNotFoundError:
            print('El archivo no existe')
        except:
            print('Ocurrió un error')

    def wol(self):
        try:
            # ssh pi@casa.theasker.ovh etherwake -i eth0 00:23:7D:07:64:DD
            # cmd = ['ssh', 'root@casa.theasker.ovh', 'ls', '-la', '/mnt/datos']
            cmd = ['ssh', 'root@casa.theasker.ovh', 'etherwake', '-i', 'eth0', '00:23:7D:07:64:DD']
            resultado = subprocess.run(cmd, capture_output=True)
            # resultado = subprocess.run(['ssh', 'root@casa.theasker.ovh', '-i', 'eth0', '00:23:7D:07:64:DD'])
            out = resultado.stdout.decode('utf-8')
            # Verificar si el comando se ejecutó correctamente
            if resultado.returncode == 0:
                self.logger.info(f"CMD: {resultado.args}")
            else:
                self.logger.error(f"CMD: {resultado.args}")
            print(out)
            return out
        except FileNotFoundError as e:
            self.logger.error(f"CMD: {cmd} {traceback.format_exc()}")
            print("Comando no existe")

if __name__ == "__main__":
    print(f"Ejecutando el fichero {__name__}")
    texto = """
    Yo para ser felíz quiero un camión
    """
    utils = Utils(f"/text2audio {texto}")
    
