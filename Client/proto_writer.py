import protobuf.ranked_pb2 as ranked
from item import Item


def item_to_protobuf(item: Item, priority: int):
    proto_item = ranked.Item()
    proto_item.value = item.value
    proto_item.priority = priority
    return proto_item


def create_package(package_id:int, command: str, proto_items: list):
    package = ranked.Package()
    package.id = package_id
    package.command = command
    for el in proto_items:
        item = package.items.add()
        item.value = el.value
        item.priority = el.priority
    return package