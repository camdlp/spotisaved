import imp
import json
import sys
from urllib import response
from wsgiref import headers
import requests
from datetime import date
from refresh import Refresh
from secrets import Secrets


# from secrets import spotify_user_id, discover_weekly_id


class SaveSongs:
    def __init__(self):
        # self.user_id = spotify_user_id
        self.spotify_token = ""
        # self.discover_weekly_id = discover_weekly_id
        self.tracks = ""
        self.new_playlist_id = ""
        self.total_tracks = 0
        self.cur_limit = 1
        self.cur_offset = 0
        self.secrets = Secrets()

    def find_songs(self):

        print("Gathering songs from my saved songs...")

        query = "https://api.spotify.com/v1/me/tracks?market=ES&limit={}&offset={}".format(self.cur_limit,
                                                                                           self.cur_offset)
        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.spotify_token)})

        response_json = response.json()
        print(response)

        self.total_tracks = response_json["total"]
        # print(response)

        for i in response_json["items"]:
            self.tracks += (i["track"]["uri"] + ",")

        # self.add_to_playlist()

    def create_playlist(self):
        print("Trying to create playlist")
        today = date.today()

        today_formatted = today.strftime("%d/%m/%Y")

        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            self.secrets.spotify_user_id)

        request_body = json.dumps({
            "name": today_formatted + " saved songs", "description": "Description of playlist", "public": True
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
        # self.new_playlist_id = self.create_playlist()

        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(self.new_playlist_id, self.tracks)
        print(self.tracks)
        response = requests.post(query,
                                 headers={"Content-Type": "application/json",
                                          "Authorization": "Bearer {}".format(self.spotify_token)
                                          })
        print(response.json)

    def iterate_find_songs(self):
        # Selecting playlist
        print("Do you want to save your song to a *new playlist(1)* or a *existing one(2)* ?...")
        ask_playlist = input("Select 1 or 2: ")
        print(ask_playlist)
        if int(ask_playlist) == 2:
            self.new_playlist_id = self.get_playlists()
        elif int(ask_playlist) == 1:
            self.new_playlist_id = self.create_playlist()

        for x in range(0, self.total_tracks):
            # for x in range(1, 101):
            self.find_songs()
            self.cur_offset += 1
            # print("\n self.cur_offset \n")

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

        refresh_caller = Refresh()

        self.spotify_token = refresh_caller.refresh()

    def find_save_songs(self):
        self.find_songs()
        self.iterate_find_songs()

    def get_playlists(self):
        # val = input("Enter your value: ")
        print("Gathering user playlists...")

        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.secrets.spotify_user_id)
        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.spotify_token)})

        response_json = response.json()

        print(response_json)

        print("Personal playlists list...")
        # Number of personal playlists found
        i = 0
        personal_playlists = []
        for playlist in response_json["items"]:
            # Gather all personal playlists
            if playlist["owner"]["display_name"] == self.secrets.spotify_user_id:
                i += 1
                personal_playlists.append(playlist)
                print(i, "-", playlist["name"])
        print("Select the playlist to save your saved tracks... (Number in the left)")
        ask_select_playlist = input("Select playlist number: ")
        print(personal_playlists[int(ask_select_playlist) - 1]["name"])
        return personal_playlists[int(ask_select_playlist) - 1]["id"]


a = SaveSongs()
a.call_refresh()
a.find_save_songs()
