import socket
import sys
sys.path.append('..')
from src import MathAlgorithm

PORT = 12357


def session(connection: socket.socket):
    help_msg = \
        b"Send an integer number (= N), then return prime numbers in [2, N) with whitespaces.\n\
Maximum value is 10^7.\n\
To disconnect, type 'exit' or blank.\n"

    with connection:
        while True:
            received = connection.recv(4096)  # fixme ストリームに残るデータにより不正な動作

            if received == b'\n' or received == b'exit\n':
                connection.sendall(b"Disconnected.\n")
                break

            if received == b'help\n':
                connection.sendall(help_msg + b"> ")
                continue

            try:
                input_val = int(received.decode())
                res = MathAlgorithm.generate_primes_str(input_val).encode()
                res += b"\n> "
                connection.sendall(res)
            except ValueError:
                connection.sendall(b"Invalid input.\n> ")


def serve():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((socket.gethostname(), PORT))
        sock.listen(5)
        while True:
            # 切断時以外では，メッセージ末尾に改行とプロンプトを表示する
            connection, address = sock.accept()
            connection.sendall(b"Connected. To see details, type 'help'.\n> ")
            session(connection)


if __name__ == '__main__':
    serve()
