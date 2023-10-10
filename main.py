import socket
import sys
import asyncio

CLIENT_SOCKET_TIMEOUT = 60

async def handle_client(client_socket, client_address):
    try:
        client_socket.settimeout(CLIENT_SOCKET_TIMEOUT)
        while True:
            data = await loop.sock_recv(client_socket, 4096)
            if not data:
                break
            try:
                decoded_data = data.decode('utf-8')
                print(f"Received data from {client_address}: {decoded_data}")
            except UnicodeDecodeError:
                print(f"Error decoding data from {client_address}")
            sys.stdout.flush()

            ack_message = "Data received and processed successfully.\n"
            await loop.sock_sendall(client_socket, ack_message.encode('utf-8'))

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
        client_socket.close()
        print(f"Connection with {client_address} closed.")
        sys.stdout.flush()

async def start_server(host, port):
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
            await loop.run_in_executor(None, handle_client, client_socket, client_address)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.stdout.flush()
    finally:
        server_socket.close()

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8080
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_server(host, port))
    except KeyboardInterrupt:
        print("\nServer terminated by user.")
        sys.stdout.flush()
        loop.run_until_complete(loop.shutdown_asyncgens())
    except Exception as e:
        print(f"Server error: {e}")
        sys.stdout.flush()
    finally:
        loop.close()
