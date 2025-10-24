import threading
import socket
import dotenv
import time
from stream_reader import StreamReader
from protobuf_reader import *

reader = StreamReader(10000)


def receive(server: socket.socket, stop_receiving):
    server.listen(5)
    while not stop_receiving.is_set():
        con, _ = server.accept()
        data = con.recv(1024)

        reader.read(data)
        messages = reader.get_storage()
        if len(messages) > 0:
            reader.clear_storage()
            for el in messages:
                try:
                    message = get_message(el)
                    print(get_items(message))
                except Exception as ex:
                    print("Cannot receive message!!!")
                    print(ex)

        con.close()


def main():
    config = dotenv.dotenv_values(".env")

    server = socket.socket()
    server.bind((config["IP"], int(config["PORT"])))

    stop_receiving = threading.Event()
    input_thread = threading.Thread(target=receive, args=(server, stop_receiving))
    input_thread.start()
    input_thread.join()


if __name__ == "__main__":
    main()