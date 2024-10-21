from typing import Iterable
from lecture_2.hw.shop_api.store.models import (
    CartEntity,
    CartInfo,
    Item
)

_cart_data = dict[int, CartInfo]()
_item_data = dict[int, Item]()


def int_id_generator() -> Iterable[int]:
    i = 0
    while True:
        yield i
        i += 1


_cart_id_generator = int_id_generator()
_item_id_generator = int_id_generator()


def get_one_cart(id: int) -> CartEntity | None:
    if id not in _cart_data:
        return None

    return CartEntity(id=id, info=_cart_data[id])

def get_one_item(id: int) -> Item | None:
    if id not in _item_data:
        return None

    return Item(id, _item_data[id]["name"], _item_data[id]["price"])

def add_cart(info: CartInfo) -> CartEntity:
    _id = next(_cart_id_generator)
    _cart_data[_id] = info

    return CartEntity(_id, info)


def add_item_to_cart(cart_id: int, item_id: int):
    _cart_data[cart_id].items.append(_item_data[item_id])

def delete_item(item_id: int):
    del _item_data[item_id]

def add_item(info: dict) -> Item:
    _id = next(_item_id_generator)
    _item_data[_id] = info

    return Item(_id, info['name'], info['price'])


def put_item(id, body):
    _item_data[id].update(body)


def patch_item(id, body):
    _item_data[id] = body


def get_many_cart(
        offset: int = 0,
        limit: int = 10,
        min_price: float = None,
        max_price: float = None,
        min_quantity: int = None,
        max_quantity: int = None
) -> Iterable[CartEntity]:
    curr = 0
    for id, info in _cart_data.items():
        if offset <= curr < offset + limit:
            result = CartEntity(id, info)
            if min_price is not None:
                if result.info.price < min_price:
                    continue
            if max_price is not None:
                if result.info.price > max_price:
                    continue
            if min_quantity is not None:
                if len(result.info.items) < min_quantity:
                    continue
            if max_quantity is not None:
                if len(result.info.items) > max_quantity:
                    continue
            yield result

        curr += 1


def get_many_item(
        offset: int = 0,
        limit: int = 10,
        min_price: float = None,
        max_price: float = None
) -> Iterable[Item]:
    curr = 0
    for id, item_data in _item_data.items():
        if offset <= curr < offset + limit:
            result = Item(id, item_data['name'], item_data['price'])
            if min_price is not None:
                if result.price < min_price:
                    continue
            if max_price is not None:
                if result.price > max_price:
                    continue
            yield result

        curr += 1