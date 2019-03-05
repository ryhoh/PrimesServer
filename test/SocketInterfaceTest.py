import unittest
import time
from multiprocessing import Process
from src.SocketInterface import *

PORT = 12357


# 複数のテストを一斉実行すると，並列実行されてポートで競合して落ちる
class SocketInterfaceTest(unittest.TestCase):

    def setUp(self):
        self.proc_server = Process(target=serve)
        self.proc_server.start()

    def tearDown(self):
        self.proc_server.terminate()

    def test_serve_message(self):
        def assertion():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((socket.gethostname(), PORT))

                recieved = sock.recv(512)
                expected = b"Connected. To see details, type 'help'.\n> "
                self.assertEqual(expected, recieved)

                sock.sendall(b'help\n')
                recieved = sock.recv(512)
                expected = b"Send an integer number (= N), then return prime \
numbers in [2, N) with whitespaces.\n\
Maximum value is 10^7.\n\
To disconnect, type 'exit' or blank.\n> "
                self.assertEqual(expected, recieved)

                sock.sendall(b'\n')
                recieved = sock.recv(512)
                expected = b"Disconnected.\n"
                self.assertEqual(expected, recieved)

        time.sleep(0.01)  # サーバの準備完了待ち
        self.proc_client = Process(target=assertion)
        self.proc_client.start()
        self.proc_client.join()

    def test_serve_invalid(self):
        def assertion():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((socket.gethostname(), PORT))

                _ = sock.recv(512)  # 最初の説明は捨て

                sock.sendall(b'abc\n')
                recieved = sock.recv(512)
                expected = b"Invalid input.\n> "
                self.assertEqual(expected, recieved)

                sock.sendall(b'3.14\n')
                recieved = sock.recv(512)
                expected = b"Invalid input.\n> "
                self.assertEqual(expected, recieved)

                sock.sendall(b'10000001\n')
                recieved = sock.recv(512)
                expected = b"Invalid input.\n> "
                self.assertEqual(expected, recieved)

                sock.sendall(b'exit\n')
                recieved = sock.recv(512)
                expected = b"Disconnected.\n"
                self.assertEqual(expected, recieved)

        time.sleep(0.01)  # サーバの準備完了待ち
        self.proc_client = Process(target=assertion)
        self.proc_client.start()
        self.proc_client.join()

    def test_serve_numeric(self):
        def assertion():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((socket.gethostname(), PORT))

                _ = sock.recv(512)  # 最初の説明は捨て

                sock.sendall(b'8\n')
                recieved = sock.recv(512)
                expected = b"2 3 5 7\n> "
                self.assertEqual(expected, recieved)

                sock.sendall(b'21\n')
                recieved = sock.recv(512)
                expected = b"2 3 5 7 11 13 17 19\n> "
                self.assertEqual(expected, recieved)

                sock.sendall(b'exit\n')
                recieved = sock.recv(512)
                expected = b"Disconnected.\n"
                self.assertEqual(expected, recieved)

        time.sleep(0.01)  # サーバの準備完了待ち
        self.proc_client = Process(target=assertion)
        self.proc_client.start()
        self.proc_client.join()

    # 受信サイズが 10Bytes だったことに対するテストケース
    def test_serve_buffer(self):
        def assertion():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((socket.gethostname(), PORT))

                _ = sock.recv(512)  # 最初の説明は捨て

                sock.sendall(b'100000000\n')
                recieved = sock.recv(512)
                expected = b"Invalid input.\n> "
                self.assertEqual(expected, recieved)

                sock.sendall(b'1000000000\n')
                recieved = sock.recv(512)
                expected = b"Invalid input.\n> "
                self.assertEqual(expected, recieved)

                sock.sendall(b'10000000000\n')
                recieved = sock.recv(512)
                expected = b"Invalid input.\n> "
                self.assertEqual(expected, recieved)

                sock.sendall(b'exit\n')
                recieved = sock.recv(512)
                expected = b"Disconnected.\n"
                self.assertEqual(expected, recieved)

        time.sleep(0.01)  # サーバの準備完了待ち
        self.proc_client = Process(target=assertion)
        self.proc_client.start()
        self.proc_client.join()


if __name__ == '__main__':
    unittest.main()  # 落ちる
