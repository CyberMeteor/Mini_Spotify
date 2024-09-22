import json
import time


# Fetch the song catalog
def create_fetch_catalog_request():
    request = {
        "type": "FETCH_CATALOG",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    }
    return json.dumps(request)


# Add a song to the playlist
def create_add_song_request(song_id):
    request = {
        "type": "ADD_SONG",
        "song_id": song_id,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    }
    return json.dumps(request)


# Remove a song from the playlist
def create_remove_song_request(song_id):
    request = {
        "type": "REMOVE_SONG",
        "song_id": song_id,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    }
    return json.dumps(request)


# Report the list of songs in the playlist in the order they appear in the playlist
def create_report_playlist_request():
    request = {
        "type": "REPORT_PLAYLIST",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())  # Adding GMT timestamp
    }
    return json.dumps(request)


# Find a song by ID from currently opened playlist
def create_find_song_request(song_id):
    request = {
        "type": "FIND_SONG",
        "song_id": song_id,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    }
    return json.dumps(request)


# Switch 3 play modes
def create_switch_mode_request(mode):
    request = {
        "type": "SWITCH_MODE",
        "mode": mode,  # e.g., "default", "shuffle", "loop"
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    }
    return json.dumps(request)


# Play the next song in the playlist
def create_play_next_request():
    request = {
        "type": "PLAY_NEXT",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    }
    return json.dumps(request)


# Go back to the previous song in the previously_played stack
def create_go_back_request():
    request = {
        "type": "GO_BACK",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    }
    return json.dumps(request)


# Use QUIT to terminate the client process
def create_quit_request():
    request = {
        "type": "QUIT",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    }
    return json.dumps(request)

