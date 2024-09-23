import json


# Parse the server's response
def parse_response(response):
    try:
        # Convert the JSON string to a Python dictionary
        response_data = json.loads(response)
        return response_data
    except json.JSONDecodeError:
        return {
            "status": "error",
            "message": "Invalid response format"
        }


# Handle a successful response
def handle_success_response(response_data):
    if "catalog" in response_data:
        # Display the song catalog
        print("\n--- Song Catalog ---")
        for song in response_data["catalog"]:
            print(
                f"ID: {song['id']}, Title: {song['song_title']}, Artist: {song['artist']}, Album: {song['album_title']}, Duration: {song['duration']}s")

    elif "playlist" in response_data:
        # Display the playlist
        print("\n--- Playlist ---")
        if len(response_data["playlist"]) > 0:
            for song in response_data["playlist"]:
                print(
                    f"ID: {song['id']}, Title: {song['song_title']}, Artist: {song['artist']}, Album: {song['album_title']}, Duration: {song['duration']}s")
        else:
            print("The playlist is currently empty.")

    elif "now_playing" in response_data:
        # Display the currently playing song
        now_playing = response_data["now_playing"]
        if now_playing:
            print(
                f"\n--- Now Playing ---\nID: {now_playing['id']}, Title: {now_playing['song_title']}, Artist: {now_playing['artist']}, Album: {now_playing['album_title']}, Duration: {now_playing['duration']}s")
        else:
            print("No song is currently playing.")

    elif "song" in response_data:
        # Display a specific song found in the playlist
        song = response_data["song"]
        print(
            f"\n--- Found Song ---\nID: {song['id']}, Title: {song['song_title']}, Artist: {song['artist']}, Album: {song['album_title']}, Duration: {song['duration']}s")

    else:
        # General success message
        print("Success: Operation completed successfully.")


# Handle an error response from the server
def handle_error_response(response_data):
    print(f"Error: {response_data.get('message', 'Unknown error occurred')}")


# Process the server's response based on the status
def process_response(response):
    response_data = parse_response(response)

    # Check the status of the response
    if response_data["status"] == "success":
        handle_success_response(response_data)
    elif response_data["status"] == "error":
        handle_error_response(response_data)
    else:
        print("Unknown response status.")
