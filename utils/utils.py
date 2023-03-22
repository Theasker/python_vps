import logging
import subprocess
import json
import traceback
import http.client

class Utils():
    def __init__(self, option):
        logging.basicConfig(
            filename='utils.log', 
            encoding='utf-8', 
            level=logging.DEBUG,
            format='%(asctime)s:  %(name)s: %(levelname)s: %(message)s', 
            datefmt='%Y/%m/%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(option)
        temp = "opcion: " + option
        self.pipedream(temp)
        if (option.startswith("/")):
            self._dispatcher(option)
    
    def pipedream(self, text):
        conn = http.client.HTTPSConnection('eolmlyay4to9iia.m.pipedream.net')
        conn.request("POST", "/", f'"test": "{text}"', {'Content-Type': 'application/json'})

    def _dispatcher(self, option):
        if (option == '/wol'):
            self.wol()
    
    def wol(self):
        try:
             # ssh pi@casa.theasker.ovh etherwake -i eth0 00:23:7D:07:64:DD
            cmd = ['ssh', 'root@casa.theasker.ovh', 'ls', '-la', '/mnt/datos']
            cmd = ['adsfds']
            resultado = subprocess.run(cmd, capture_output=True)
            # resultado = subprocess.run(['ssh', 'root@casa.theasker.ovh', '-i', 'eth0', '00:23:7D:07:64:DD'])
            out = resultado.stdout.decode('utf-8')
            # Verificar si el comando se ejecutó correctamente
            if resultado.returncode == 0:
                self.logger.info(f"CMD: {resultado.args}")
            else:
                self.logger.error(f"CMD: {resultado.args}")
            return out
        except FileNotFoundError as e:
            self.logger.error(f"CMD: {cmd} {traceback.format_exc()}")

    def pruebas(self):
        self.logger.info("prueba")

if __name__ == "__main__":
    utils = Utils("wol")
    utils.pruebas()