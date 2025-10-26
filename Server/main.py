import threading
import socket
from threading import Thread

import dotenv
import time
from stream_reader import StreamReader
from protobuf_reader import *

reader = StreamReader(10000)


def output_items(items:list):
    if not items:
        return
    items.sort(key=lambda x: x["group"])

    group_num = None
    counter = 0
    for el in items:
        if group_num != el["group"]:
            group_num = el["group"]
            counter = 1
            print(f"Group №{group_num}")

        print(f"Element №{counter}")
        print(f"Priority: {el["priority"]}")
        print(f"Value: {el["value"]}")
        counter += 1


def handle_connection(con, abort_connection, retry=5):
    print("Handling connection")
    cnt = 0
    while not abort_connection.is_set() and cnt < retry:
        try:
            data = con.recv(1024)
            if len(data) == 0:
                cnt += 1
                continue
            cnt = 0
        except Exception as ex:
            cnt += 1
            continue

        reader.read(data)
        messages = reader.get_storage()
        if len(messages) > 0:
            reader.clear_storage()
            for el in messages:
                try:
                    message = get_message(el)
                    con.send("#ACCEPTED#".encode())
                    output_items(get_items(message))
                    if message.command == "ABORT":
                        abort_connection.set()
                        return
                except Exception as ex:
                    con.send("#ERROR#".encode())
                    print("Cannot receive message!!!")
                    print(ex)

        time.sleep(1)
    abort_connection.set()


def receive_connection(server: socket.socket, stop_receiving, retry=90):
    server.listen()
    connections = dict()
    while not stop_receiving.is_set():
        to_remove = []
        for conn in connections.keys():
            if connections[conn].is_set():
                to_remove.append(conn)
        for conn in to_remove:
            connections.pop(conn)
            print("Connection aborted...")

        try:
            con, addr = server.accept()
        except Exception as ex:
            continue
        abort_connection = threading.Event()
        connections[con] = abort_connection

        connection_thread = threading.Thread(target=handle_connection, args=(con, abort_connection))
        connection_thread.start()
        print(f"Established connection with {addr}")


def main():
    config = dotenv.dotenv_values(".env")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((config["IP"], int(config["PORT"])))
    server.settimeout(5)

    stop_receiving = threading.Event()
    input_thread = threading.Thread(target=receive_connection, args=(server, stop_receiving))
    input_thread.start()

    print("Server starting!!!")

    input_thread.join()


if __name__ == "__main__":
    main()