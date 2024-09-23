#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Mini_Spotify
@File    ：server.py
@Author  ：Ruiyang Chen
"""

import socket
import json
import time
import random

HOST = 'localhost'
PORT = 12000


# Load catalog.json into memory
def load_catalog():
    with open('catalog.json', 'r') as file:
        catalog = json.load(file)
    return catalog


playlist = []
play_mode_playlist = []  # Copy of the playlist for play mode
previously_played = []  # Stack to track previously dequeued songs
now_playing = None
submode = "default"  # default, shuffle, loop


# Response for FETCH_CATALOG
def fetch_catalog_response():
    catalog = load_catalog()
    response = {
        "status": "success",
        "catalog": catalog['catalog'],
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    }
    return json.dumps(response)


# Add a song to the playlist
def add_song(song_id):
    catalog = load_catalog()
    for song in catalog['catalog']:
        if song['id'] == song_id:
            playlist.append(song)
            return json.dumps({
                "status": "success",
                "message": f"Song {song_id} added to the playlist",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            })
    return json.dumps({
        "status": "error",
        "message": f"Invalid song ID: {song_id}",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    })


# Remove a song from the playlist
def remove_song(song_id):
    for song in playlist:
        if song['id'] == song_id:
            playlist.remove(song)
            return json.dumps({
                "status": "success",
                "message": f"Song {song_id} removed from the playlist",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            })
    return json.dumps({
        "status": "error",
        "message": f"Song with ID {song_id} not found in playlist",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    })


# Report playlist in design mode
def report_playlist():
    if len(playlist) > 0:
        return json.dumps({
            "status": "success",
            "playlist": playlist,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        })
    else:
        return json.dumps({
            "status": "error",
            "message": "The playlist is empty",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        })


# Find a song by its ID in the playlist
def find_song_by_id(song_id):
    for song in playlist:
        if song['id'] == song_id:
            return json.dumps({
                "status": "success",
                "message": f"Song with ID {song_id} found in the playlist.",
                "song": song,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            })
    return json.dumps({
        "status": "error",
        "message": f"Song with ID {song_id} not found in the playlist.",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    })


# Switch to play mode
def switch_to_play_mode(mode):
    global play_mode_playlist, submode, now_playing
    play_mode_playlist = playlist.copy()
    submode = mode

    if submode == "shuffle":
        random.shuffle(play_mode_playlist)

    if len(play_mode_playlist) > 0:
        now_playing = play_mode_playlist.pop(0)
        if submode == "loop":
            play_mode_playlist.append(now_playing)
    else:
        now_playing = None

    return json.dumps({
        "status": "success",
        "message": f"Switched to play mode with {submode} submode",
        "now_playing": now_playing,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    })


# Handle play mode commands
def play_next():
    global now_playing, previously_played
    if len(play_mode_playlist) > 0:
        if now_playing:
            previously_played.append(now_playing)
        now_playing = play_mode_playlist.pop(0)
        if submode == "loop":
            play_mode_playlist.append(now_playing)
        return json.dumps({
            "status": "success",
            "now_playing": now_playing,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        })
    return json.dumps({
        "status": "error",
        "message": "No more songs in the playlist",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    })


# Go back to the previous song
def go_back():
    global now_playing
    if previously_played:
        # Restore the last played song from the previously_played stack
        previous_song = previously_played.pop()

        # Place the current song back at the front of the playlist (if not already None)
        if now_playing:
            playlist.insert(0, now_playing)

        # Update now_playing to the restored song
        now_playing = previous_song

        return json.dumps({
            "status": "success",
            "message": f"Restored previous song: {now_playing['song_title']}",
            "now_playing": now_playing,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        })
    else:
        return json.dumps({
            "status": "error",
            "message": "No previously played song to go back to",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        })


# Report the current song playing
def report_now_playing():
    if now_playing:
        return json.dumps({
            "status": "success",
            "now_playing": now_playing,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        })
    else:
        return json.dumps({
            "status": "error",
            "message": "No song is currently playing",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        })


# Main server
def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Server is listening on {HOST}:{PORT}...")

    while True:
        connection_socket, addr = server_socket.accept()
        print(f"Connected to {addr}")

        try:
            request = connection_socket.recv(1024).decode('utf-8')
            request_data = json.loads(request)

            response = {}
            if request_data["type"] == "FETCH_CATALOG":
                response = fetch_catalog_response()
            elif request_data["type"] == "ADD_SONG":
                response = add_song(request_data["song_id"])
            elif request_data["type"] == "REMOVE_SONG":
                response = remove_song(request_data["song_id"])
            elif request_data["type"] == "REPORT_PLAYLIST":
                response = report_playlist()
            elif request_data["type"] == "FIND_SONG":
                response = find_song_by_id(request_data["song_id"])
            elif request_data["type"] == "SWITCH_TO_PLAY":
                response = switch_to_play_mode(request_data["submode"])
            elif request_data["type"] == "PLAY_NEXT":
                response = play_next()
            elif request_data["type"] == "GO_BACK":
                response = go_back()
            elif request_data["type"] == "REPORT_NOW_PLAYING":
                response = report_now_playing()
            else:
                response = json.dumps({
                    "status": "error",
                    "message": "Invalid request type",
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                })

            connection_socket.send(response.encode('utf-8'))

        except json.JSONDecodeError:
            # Handle JSON decode errors
            error_response = json.dumps({
                "status": "error",
                "message": "Invalid request format",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            })
            connection_socket.send(error_response.encode('utf-8'))

        except Exception as e:
            # Handle any other server errors
            error_response = json.dumps({
                "status": "error",
                "message": f"Server error: {str(e)}",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            })
            connection_socket.send(error_response.encode('utf-8'))

        finally:
            connection_socket.close()


if __name__ == "__main__":
    run_server()
