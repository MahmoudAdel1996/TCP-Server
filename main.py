import socket
import logging
import threading

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

            # Decode the received data and split it into headers and body
            data_str = data.decode('utf-8')
            headers, body = data_str.split('\r\n\r\n', 1)

            # Log the headers and the received data
            logger.info(f"Received headers from {client_address}:\n{headers}")
            logger.info(f"Received data from {client_address}:\n{body}")

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
    host = "0.0.0.0"  # Change to your desired host
    port = 8080  # Change to your desired port

    start_tcp_server(host, port)
