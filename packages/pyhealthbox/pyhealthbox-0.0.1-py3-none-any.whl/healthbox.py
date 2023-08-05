import requests
from socket import *

class HealthBox():

    def __init__(self, ip_address=""):
        # 192.168.0.213
        if ip_address == "":
            self.ip_address = discover_healthbox()
        else:
            self.ip_address = ip_address

    def discover_healthbox(self):
        pass
    
    def get_air_quality_index(self):
        endpoint = 'http://' + self.ip_address + '/v1/api/data/current'
        hb_response = requests.get(url=endpoint).json()
        gaqi = hb_response['sensor'][0]['parameter']['index']['value']
        return gaqi
