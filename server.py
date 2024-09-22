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

# Define the server-side playlist and mode
playlist = []
mode = "design"  # initial mode
submode = "default"
now_playing = None


# Response for FETCH_CATALOG
def fetch_catalog_response():
    catalog = load_catalog()
    response = {
        "status": "success",
        "catalog": catalog['catalog'],
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    }
    return json.dumps(response)


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


# Switch to play mode
def switch_to_play_mode(mode):
    global submode, now_playing
    submode = mode

    if len(playlist) > 0:
        if submode == "shuffle":
            random.shuffle(playlist)
        now_playing = playlist[0]

    return json.dumps({
        "status": "success",
        "message": f"Switched to play mode with {submode} submode",
        "now_playing": now_playing,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    })

# Handle play mode commands
def play_next():
    global now_playing
    if len(playlist) > 0:
        now_playing = playlist.pop(0)
        if submode == "loop":
            playlist.append(now_playing)
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


# Main server
def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Server is listening on {HOST}:{PORT}...")

    while True:
        connection_socket, addr = server_socket.accept()
        print(f"Connected to {addr}")
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
        elif request_data["type"] == "SWITCH_TO_PLAY":
            response = switch_to_play_mode(request_data["submode"])
        elif request_data["type"] == "PLAY_NEXT":
            response = play_next()
        else:
            response = json.dumps({
                "status": "error",
                "message": "Invalid request",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            })

        connection_socket.send(response.encode('utf-8'))
        connection_socket.close()


if __name__ == "__main__":
    run_server()
