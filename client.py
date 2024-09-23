import socket
import json
import request
import response

HOST = 'localhost'
PORT = 12000


# Send a request and receive the response
def send_request(request_data):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        client_socket.send(request_data.encode('utf-8'))
        server_response = client_socket.recv(4096).decode('utf-8')
        client_socket.close()
        return server_response
    except Exception as e:
        print(f"Error: {e}")
        return None


# Display the song catalog
def display_catalog(catalog):
    print("\n--- Song Catalog ---")
    for song in catalog:
        print(
            f"ID: {song['id']}, Title: {song['song_title']}, Artist: {song['artist']}, Album: {song['album_title']}, Duration: {song['duration']}s")


# Main client
def run_client():
    mode = "design"
    while True:
        print("\nMenu:")
        if mode == "design":
            print("1. Fetch Catalog")
            print("2. Add Song to Playlist")
            print("3. Remove Song from Playlist")
            print("4. Report Playlist")
            print("5. Find Song in Playlist by ID")
            print("6. Switch to Play Mode")
            print("7. Quit")
        elif mode == "play":
            print("1. Play Next Song")
            print("2. Go Back")
            print("3. Report Now Playing")
            print("4. Switch to Design Mode")
            print("5. Quit")

        choice = input("Enter your choice: ")

        if mode == "design":
            if choice == '1':
                response_data = send_request(request.create_fetch_catalog_request())
                response.process_response(response_data)

            elif choice == '2':
                song_id = int(input("Enter Song ID to add: "))
                response_data = send_request(request.create_add_song_request(song_id))
                response.process_response(response_data)

            elif choice == '3':
                song_id = int(input("Enter Song ID to remove: "))
                response_data = send_request(request.create_remove_song_request(song_id))
                response.process_response(response_data)

            elif choice == '4':
                response_data = send_request(request.create_report_playlist_request())
                response.process_response(response_data)

            elif choice == '5':
                song_id = int(input("Enter Song ID to find: "))
                response_data = send_request(request.create_find_song_request(song_id))
                response.process_response(response_data)

            elif choice == '6':
                submode = input("Enter submode (default/shuffle/loop): ")
                response_data = send_request(request.create_switch_mode_request(submode))
                response.process_response(response_data)
                mode = "play"  # Switch to play mode

            elif choice == '7':
                print("Exiting...")
                break

        elif mode == "play":
            if choice == '1':
                response_data = send_request(request.create_play_next_request())
                response.process_response(response_data)

            elif choice == '2':
                response_data = send_request(request.create_go_back_request())
                response.process_response(response_data)

            elif choice == '3':
                response_data = send_request(request.create_report_now_playing_request())
                response.process_response(response_data)

            elif choice == '4':
                print("Switching to design mode...")
                mode = "design"  # Switch back to design mode

            elif choice == '5':
                print("Exiting...")
                break


if __name__ == "__main__":
    run_client()
