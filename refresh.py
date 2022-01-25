from email.mime import base
import requests
import json
from secrets import Secrets


class Refresh:

    def __init__(self):
        #self.refresh_token = refresh_token
        #self.base_64 = base_64
        self.s = Secrets()

    def refresh(self):
        query = "https://accounts.spotify.com/api/token"
        response = requests.post(query,
                                 data={"grant_type": "refresh_token", "refresh_token": self.s.refresh_token},
                                 headers={"Authorization": "Basic " + self.s.base_64})
        response_json = response.json()
        print(response_json)
        return response_json["access_token"]
