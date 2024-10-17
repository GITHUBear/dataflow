import socket
import random
import time
from typing import List, Tuple
import argparse

class SocketDataProducer:
    def __init__(
        self, 
        file: str,
        miu_interval: int,
        delta_interval: int, 
        server_host: str,
        server_port: int,
    ):
        if delta_interval > miu_interval:
            raise ValueError("delta_interval must less than miu_interval")
        
        self.file = file
        self.miu_interval = miu_interval
        self.delta_interval = delta_interval

        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((server_host, server_port))
    
    def product(self):
        print(f"process-{self.file}: begin product")
        # for (x, y) in self.data:
        with open(self.file, 'r') as f:
            for line in f:
                x, y = map(float, line.strip().split(' '))
                delta = random.randint(-self.delta_interval, self.delta_interval)
                time.sleep((self.miu_interval + delta) / 1000.0)
                data = f"{self.file} {x} {y}\n"
                self.conn.sendall(data.encode())
                print(f"process-{self.file}: [finish] send ({x}, {y})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True)
    parser.add_argument('-m', '--miu_interval', type=int, default=2000)
    parser.add_argument('-d', '--delta_interval', type=int, default=1000)
    parser.add_argument('-H', '--host', type=str, default='localhost')
    parser.add_argument('-p', '--port', type=str, default=12345)

    args = parser.parse_args()

    producer = SocketDataProducer(
        args.file,
        args.miu_interval,
        args.delta_interval,
        args.host,
        args.port,
    )

    producer.product()