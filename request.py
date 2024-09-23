#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Mini_Spotify
@File    ：request.py
@Author  ：Ruiyang Chen
"""
import json
import time


# Helper function to create metadata for the request
def create_request_metadata(request_type, url="/", method="GET"):
    return {
        "method": method,  # HTTP-like method: GET, POST, PUT
        "url": url,
        "version": "HTTP/1.1",
        "type": request_type,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    }


# Fetch the song catalog
def create_fetch_catalog_request():
    request = create_request_metadata("FETCH_CATALOG", url="/catalog", method="GET")
    return json.dumps(request)


# Add a song to the playlist
def create_add_song_request(song_id):
    request = create_request_metadata("ADD_SONG", url=f"/playlist/{song_id}", method="POST")
    request["song_id"] = song_id
    return json.dumps(request)


# Remove a song from the playlist
def create_remove_song_request(song_id):
    request = create_request_metadata("REMOVE_SONG", url=f"/playlist/{song_id}", method="DELETE")
    request["song_id"] = song_id
    return json.dumps(request)


# Report the list of songs in the playlist in the order they appear in the playlist
def create_report_playlist_request():
    request = create_request_metadata("REPORT_PLAYLIST", url="/playlist", method="GET")
    return json.dumps(request)


# Find a song by ID from the currently opened playlist
def create_find_song_request(song_id):
    request = create_request_metadata("FIND_SONG", url=f"/playlist/{song_id}", method="GET")
    request["song_id"] = song_id
    return json.dumps(request)


# Switch between 3 play modes
def create_switch_mode_request(submode):
    request = create_request_metadata("SWITCH_TO_PLAY", url="/playmode", method="POST")
    request["submode"] = submode  # e.g., "default", "shuffle", "loop"
    return json.dumps(request)


# Play the next song in the playlist
def create_play_next_request():
    request = create_request_metadata("PLAY_NEXT", url="/playlist/next", method="POST")
    return json.dumps(request)


# Go back to the previous song in the previously_played stack
def create_go_back_request():
    request = create_request_metadata("GO_BACK", url="/playlist/back", method="POST")
    return json.dumps(request)


# Request the currently playing song
def create_report_now_playing_request():
    request = create_request_metadata("REPORT_NOW_PLAYING", url="/playlist/nowplaying", method="GET")
    return json.dumps(request)


# Use QUIT to terminate the client process
def create_quit_request():
    request = create_request_metadata("QUIT", url="/quit", method="POST")
    return json.dumps(request)
