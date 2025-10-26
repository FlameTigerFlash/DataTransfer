import protobuf.ranked_pb2 as ranked


def get_message(string:bytes):
    message = ranked.Package()
    message.ParseFromString(string)
    return message


def get_items(message):
    items = []

    for el in message.items:
        new_item = dict()
        new_item["value"] = el.value
        new_item["priority"] = el.priority
        new_item["group"] = message.id
        items.append(new_item)

    return items