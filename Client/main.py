import socket
import dotenv
import threading
import time
import math
import random
from proto_writer import *


def client_connect(client, ip: str, port: int):
    try:
        client.connect((ip, port))
    except Exception as ex:
        print("Cannot connect")
        print(ex)
        return False
    return True


def send_package(client, package):
    message = b"#S#" + package.SerializeToString() + b"#E#"
    client.send(message)


def main():
    config = dotenv.dotenv_values(".env")

    client = socket.socket()
    connected = client_connect(client, config["IP"], int(config["PORT"]))
    if not connected:
        return

    items = []
    for i in range(random.randint(3, 8)):
        new_item = Item(random.randint(-20, 20))
        items.append(new_item)

    items.sort(key=lambda item: abs(math.sin(item.value)))
    proto_items = [item_to_protobuf(items[i], i) for i in range(len(items))]
    package = create_package(package_id=0, command="ADD", proto_items=proto_items)

    try:
        send_package(client, package)
    except Exception as ex:
        print("Cannot send message!!!")
        print(ex)

    client.close()


if __name__ == "__main__":
    main()