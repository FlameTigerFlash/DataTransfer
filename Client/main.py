import socket
import dotenv
import threading
import time
import math
import random
from proto_writer import *

message_accepted = True


def client_connect(client, ip: str, port: int, attempts = 20, interval = 2):
    for i in range(attempts):
        print(f"Connection attempt № {i+1}")
        try:
            client.connect((ip, port))
            print("Client connected successfully!!!")
            return True
        except Exception as ex:
            print("Cannot connect...")
            print(ex)
        time.sleep(interval)
    return False


def send_package(client, package):
    message = b"#S#" + package.SerializeToString() + b"#E#"
    client.send(message)


def wait_for_reply(client: socket.socket, stop_receiving):
    global message_accepted
    message_accepted = False
    while not stop_receiving.is_set():
        try:
            data = client.recv(1024)
        except Exception as ex:
            return

        text = data.decode()
        if "#ACCEPTED#" in text and not stop_receiving.is_set():
            print("Message accepted")
            message_accepted =  True
            return


def main():
    global message_accepted

    error_limit  = 20

    config = dotenv.dotenv_values(".env")
    #client.settimeout(50)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = client_connect(client, 'server', int(config["PORT"]))
    if not connected:
        print("Cannot connect... Finishing program.")
        return

    cnt = 0
    package_id = 0
    while True:
        if cnt >= error_limit:
            client = socket.socket()
            connected = client_connect(client, config["IP"], int(config["PORT"]))
            if not connected:
                print("Cannot connect... Finishing program.")
                return

        items = []
        for i in range(random.randint(3, 8)):
            new_item = Item(random.randint(-20, 20))
            items.append(new_item)

        items.sort(key=lambda item: abs(math.sin(item.value)))
        proto_items = [item_to_protobuf(items[i], i) for i in range(len(items))]
        package = create_package(package_id=package_id, command="ADD", proto_items=proto_items)

        try:
            message_accepted = False
            while not message_accepted:
                send_package(client, package)

                stop_receiving = threading.Event()
                input_thread = threading.Thread(target=wait_for_reply, args=(client, stop_receiving))
                input_thread.start()

                time.sleep(3)
                stop_receiving.set()

                if message_accepted:
                    print(f"Package {package_id} delivered!")
                    package_id += 1
                else:
                    print(f"Package {package_id} lost...")
            cnt = 0

        except Exception as ex:
            cnt += 1
            print("Cannot send message!!!")
            print(ex)

        time.sleep(2)

if __name__ == "__main__":
    main()