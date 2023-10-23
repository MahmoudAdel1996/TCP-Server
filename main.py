import socket
import sys
import threading

CLIENT_SOCKET_TIMEOUT = 60
BUFFER_SIZE = 4096

# Lock for protecting shared resources (if any)
lock = threading.Lock()

# List to keep track of active client threads
active_threads = []

def handle_client(client_socket, client_address):
    try:
        client_socket.settimeout(CLIENT_SOCKET_TIMEOUT)
        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            try:
                decoded_data = data.decode('utf-8')
                print(f"Received data from {client_address}: {decoded_data}")
            except UnicodeDecodeError:
                print(f"Error decoding data from {client_address}")
            sys.stdout.flush()

            ack_message = "Data received and processed successfully.\n"
            client_socket.send(ack_message.encode('utf-8'))

    except ConnectionResetError:
        print(f"Connection reset by {client_address}")
        sys.stdout.flush()
    except socket.timeout:
        print(f"Client connection timed out")
        sys.stdout.flush()
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
        sys.stdout.flush()
    finally:
        # Close the client socket
        client_socket.close()
        print(f"Connection with {client_address} closed.")
        sys.stdout.flush()
        # Remove the current thread from the active_threads list
        with lock:
            active_threads.remove(threading.current_thread())

def start_server(host, port):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server listening on {host}:{port}")
        sys.stdout.flush()
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")
            sys.stdout.flush()

            # Create a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
            # Add the new thread to the active_threads list
            with lock:
                active_threads.append(client_thread)

    except Exception as e:
        print(f"Error starting server: {e}")
        sys.stdout.flush()
    finally:
        server_socket.close()

def stop_server():
    # Stop all active threads
    with lock:
        for thread in active_threads:
            thread.join()

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8080
    try:
        start_server(host, port)
    except KeyboardInterrupt:
        print("\nServer terminated by user.")
        sys.stdout.flush()
        stop_server()  # Stop all active threads
        sys.exit(0)
    except Exception as e:
        print(f"Server error: {e}")
        stop_server()  # Stop all active threads
        sys.stdout.flush()
