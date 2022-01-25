import requests
import json

# spotify_token = "BQArjroVIKHfXJG6kWYmPJIG32t6C7x8C1y3eUlZ-WDmqPuWjpj9mysJO1w4hDf8A5qPoz84Sxz8u_-xMncYeJ2PhXC65qFpifu5o_OUpWf5Nblo4DQ9vVPeEmJNPu1nWMjS3Ry_d-_k5ZmjGN-tQOwY_AbKfAjSIEIyha0"
# spotify_user_id = "carlosabiamerino"
# discover_weekly_id = "3sgGOPs7p2nvVdqxbmdoYy"
# refresh_token = "AQAl92RXngk4h0P4X8GY_b-9wa2bERq1G74iwpSbnsDY1nQuu5MvaGQYOIz7UdvuC6pFwhtD6dUtP5RJQbmf1UJNt48U8O_ct_A7e9iIgmm4v60NHZiPF8BVy7Jdri5fQEk"
# base_64 = "ZTg5ZGYxOGFjZDNkNDc2YWFiYjFiMzVkZDhlMWRkNjk6ZjVlMWVmZGI5N2U3NDJkMDhhYjc4NTI0NmQ4OWE2NDQ"


class Secrets:
    def __init__(self):
        self.spotify_token = ""
        self.spotify_user_id = ""
        self.playlist_target_id = ""
        self.refresh_token = ""
        self.base_64 = ""
        self.read_config()

    def read_config(self):
        f = open('info.json')
        data = json.load(f)
        self.spotify_token = data["spotify_token"]
        self.spotify_user_id = data["spotify_user_id"]
        self.playlist_target_id = data["playlist_target_id"]
        self.refresh_token = data["refresh_token"]
        self.base_64 = data["base_64"]
