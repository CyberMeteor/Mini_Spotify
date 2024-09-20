import socket
import json

HOST = 'localhost'
PORT = 12000


# Send a request and receive the response
def send_request(request):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")

        client_socket.send(request.encode('utf-8'))
        print(f"Sent request: {request}")

        response = client_socket.recv(4096).decode('utf-8')
        response_data = json.loads(response)
        return response_data

    except Exception as e:
        print(f"Error occurred: {e}")
        return None
    finally:
        client_socket.close()


# Display the song catalog
def display_catalog(catalog):
    print("\n--- Song Catalog ---")
    for song in catalog:
        print(
            f"ID: {song['id']}, Title: {song['song_title']}, Artist: {song['artist']}, Album: {song['album_title']}, Duration: {song['duration']}s")


# Main client
def run_client():
    while True:
        print("\nMenu:")
        print("1. Fetch Song Catalog")
        print("2. Quit")

        choice = input("Enter your choice: ")
        if choice == '1':
            request = "FETCH_CATALOG"
            response = send_request(request)

            if response and response["status"] == "success":
                display_catalog(response["catalog"])
            else:
                print("Failed to fetch catalog or invalid response.")
        elif choice == '2':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    run_client()
