from dataclasses import dataclass


@dataclass
class ItemInfo:
    name: str
    price: float

@dataclass
class Item:
    id: int
    name: str
    price: float

@dataclass
class CartInfo:
    items: list[Item]
    price: float
    published: bool


@dataclass
class CartEntity:
    id: int
    info: CartInfo

