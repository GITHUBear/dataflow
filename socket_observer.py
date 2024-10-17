import socket
import threading
import argparse
from filelock import FileLock

def write_data_local(data: str):
    strs = data.strip().split(' ')
    tmp_file = f"{strs[0]}.tmp"
    lock_file = f"{tmp_file}.lock"
    with FileLock(lock_file):
        with open(tmp_file, 'a') as f:
            f.write(f"{float(strs[1])} {float(strs[2])}\n")

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            d = data.decode()
            print(f"Received: {d}")
            write_data_local(d)
        except Exception as e:
            print(f"Error: {e}")
            break
    client_socket.close()

def start_server(host='0.0.0.0', port=9999):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(10)
    print(f"Server listening on {host}:{port}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    finally:
        server_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', type=str, default='0.0.0.0')
    parser.add_argument('-p', '--port', type=int, default=12345)

    args = parser.parse_args()

    start_server(args.host, args.port)
