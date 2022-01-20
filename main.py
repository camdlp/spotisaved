import imp
import json
from urllib import response
from wsgiref import headers
import requests
from secrets import spotify_user_id,discover_weekly_id 
from datetime import date
from refresh import Refresh

class SaveSongs: 
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = ""
        self.discover_weekly_id = discover_weekly_id
        self.tracks = ""
        self.new_playlist_id = ""
        self.total_tracks = 0
        self.cur_limit = 1
        self.cur_offset = 0
        
    def find_songs(self):
        
        print("Gathering songs from my saved songs...")
        
        query = "https://api.spotify.com/v1/me/tracks?market=ES&limit={}&offset={}".format(self.cur_limit, self.cur_offset)
        response = requests.get(query, 
                                headers={"Content-Type": "application/json",
                                "Authorization": "Bearer {}".format(self.spotify_token)})
        
        response_json = response.json()
        print(response)
        
        self.total_tracks = response_json["total"]
        #print(response)
        
        for i in response_json["items"]:
            self.tracks += (i["track"]["uri"] + ",")
        
        
        #self.add_to_playlist()
        
    def create_playlist(self):
        print("Trying to create playlist")
        today = date.today()
        
        todayFormatted = today.strftime("%d/%m/%Y")
        
        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotify_user_id)
        
        request_body = json.dumps({
            "name": todayFormatted + " saved songs", "description": "Description of playlist", "public": True
        })
        
        response = requests.post(query, 
                               data=request_body, 
                               headers={"Content-Type": "application/json",
                                "Authorization": "Bearer {}".format(self.spotify_token)
                                })
        response_json = response.json()
        return response_json["id"]
        
    def add_to_playlist(self):
        # add all songs to playlist
        #self.new_playlist_id = self.create_playlist()
        
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(self.new_playlist_id, self.tracks)
        print(self.tracks)
        response = requests.post(query, 
                                 headers={"Content-Type": "application/json",
                                "Authorization": "Bearer {}".format(self.spotify_token)
                                })
        print(response.json)
        
    def iterate_find_songs(self):
        # Creating playlist
        self.new_playlist_id = self.create_playlist()
        
        for x in range(0, self.total_tracks):
        #for x in range(1, 101):    
            self.find_songs()
            self.cur_offset += 1
            #print("\n self.cur_offset \n")

            # Saves songs every 100 searches
            if x % 50 == 0:
                print("\nSaving...\n")
                self.tracks = self.tracks[:-1]
                self.add_to_playlist()
                self.tracks *= 0
        
        self.tracks = self.tracks[:-1]
        print(self.tracks)
        self.add_to_playlist()
        
    
    def call_refresh(self):
        print("Refreshing token")
        
        refreshCaller = Refresh()
        
        self.spotify_token = refreshCaller.refresh()
        
        self.find_songs()
        self.iterate_find_songs()
    
        
a = SaveSongs()
a.call_refresh()

        
        