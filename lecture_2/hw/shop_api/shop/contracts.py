from pydantic import BaseModel
from lecture_2.hw.shop_api.store.models import (
    CartInfo,
    CartEntity,
    Item,
    ItemInfo
)


class CartResponse(BaseModel):
    id: int
    items: list[Item]
    price: float
    published: bool

    @staticmethod
    def from_entity(entity: CartEntity):
        return CartResponse(
            id=entity.id,
            items=entity.info.items,
            price=entity.info.price,
            published=entity.info.published,
        )


class CartRequest(BaseModel):
    items: list[Item]
    price: float
    published: bool

    def as_cart_info(self) -> CartInfo:
        return CartInfo(items=self.items, price=self.price, published=self.published)
