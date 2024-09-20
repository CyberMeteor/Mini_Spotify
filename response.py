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
        print("\n--- Song Catalog ---")
        for song in response_data["catalog"]:
            print(f"ID: {song['id']}, Title: {song['song_title']}, Artist: {song['artist']}, Album: {song['album_title']}, Duration: {song['duration']}s")
    else:
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
