import socket
import threading
import sys

# Define the server's host and port
HOST = '0.0.0.0'  # Listen on all available network interfaces
PORT = 8080      # Choose a port for your server (e.g., 8080)

def main():
    # Create a TCP socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # Bind the socket to the host and port
            server_socket.bind((HOST, PORT))

            # Listen for incoming connections
            server_socket.listen()

            sys.stdout.write(f"Server is listening on {HOST}:{PORT}\n")
            sys.stdout.flush()

            while True:
                # Accept a client connection
                client_socket, client_address = server_socket.accept()
                sys.stdout.write(f"Accepted connection from {client_address}\n")
                sys.stdout.flush()

                # Create a new thread to handle the client connection
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
                client_thread.start()
    except Exception as e:
        sys.stderr.write(f"An error occurred: {e}\n")
        sys.stderr.flush()
        sys.exit(1)

def handle_client(client_socket, client_address):
    with client_socket:
        try:
            while True:
                # Receive data from the client
                data = client_socket.recv(1024)

                if not data:
                    break  # No more data from the client, disconnect

                # Process the received data (customize this part for your application)
                # For now, we'll just echo the data back to the client
                sys.stdout.write(f"Received data from {client_address}: {data.decode('utf-8')}\n")
                sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"An error occurred while handling the client connection: {e}\n")
            sys.stderr.flush()

if __name__ == "__main__":
    main()