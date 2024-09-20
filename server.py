import socket
import json
import time

HOST = 'localhost'
PORT = 12000


# Load catalog.json into memory
def load_catalog():
    with open('catalog.json', 'r') as file:
        catalog = json.load(file)
    return catalog


# Create a response for FETCH_CATALOG
def fetch_catalog_response():
    catalog = load_catalog()
    response = {
        "status": "success",
        "catalog": catalog['catalog'],
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    }
    return json.dumps(response)


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
        print(f"Received request: {request}")

        if request == "FETCH_CATALOG":
            response = fetch_catalog_response()
        else:
            response = json.dumps({
                "status": "error",
                "message": "Invalid request",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            })

        connection_socket.send(response.encode('utf-8'))
        print(f"Sent response: {response}")

        connection_socket.close()


if __name__ == "__main__":
    run_server()
