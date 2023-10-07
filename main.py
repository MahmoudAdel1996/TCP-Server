import socket
import logging
import threading
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('TCP_Server')

def handle_client(client_socket, client_address):
    try:
        logger.info(f"Accepted connection from {client_address}")

        while True:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break

            # Decode the received data as JSON
            try:
                json_data = json.loads(data.decode('utf-8'))
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON data from {client_address}: {e}")
                continue

            # Log the received JSON data
            logger.info(f"Received JSON data from {client_address}:\n{json.dumps(json_data, indent=4)}")

            # Send a response back to the client (optional)
            # client_socket.send(b"Data received")

    except Exception as e:
        logger.error(f"Error handling client {client_address}: {e}")
    finally:
        # Close the client socket
        client_socket.close()
        logger.info(f"Connection with {client_address} closed")

def start_tcp_server(host, port):
    try:
        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the address and port
        server_socket.bind((host, port))

        # Listen for incoming connections
        server_socket.listen(5)
        logger.info(f"Listening on {host}:{port}")

        while True:
            # Accept a connection from a client
            client_socket, client_address = server_socket.accept()

            # Start a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()

    except Exception as e:
        logger.error(f"Error starting server: {e}")
    finally:
        # Close the server socket
        server_socket.close()

if __name__ == "__main__":
    host = "0.0.0.0"  # Listen on all available network interfaces
    port = 8080  # Use port 8080

    start_tcp_server(host, port)
