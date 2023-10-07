import socket
import sys
import threading

def handle_client(client_socket, client_address):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Received data from {client_address}: {data.decode('utf-8')}")
            sys.stdout.flush()
            
            # Continue listening for the next message
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"Connection with {client_address} closed.")

def start_server(host, port):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server listening on {host}:{port}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")
            
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.stdout.flush()
    finally:
        server_socket.close()

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8080
    try:
        start_server(host, port)
    except KeyboardInterrupt:
        print("\nServer terminated by user.")
        sys.stdout.flush()
        sys.exit(0)
    except Exception as e:
        print(f"Server error: {e}")
        sys.stdout.flush()
