import socket
import sys

def start_server(host, port):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        while True:
            client_socket, client_address = server_socket.accept()
            try:
                client_socket.settimeout(25)  # Set a 25-second timeout for receiving data
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Received data from {client_address}: {data.decode('utf-8')}")
                sys.stdout.flush()
            except socket.timeout:
                print(f"No data received from {client_address} within 25 seconds. Closing connection.")
                sys.stdout.flush()
            except Exception as e:
                print(f"Error handling client {client_address}: {e}")
                sys.stdout.flush()
            finally:
                client_socket.close()
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
