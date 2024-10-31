from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import NonNegativeInt, PositiveInt, PositiveFloat
from lecture_2.hw.shop_api import store
from pydantic.types import Json
from typing import Optional, Dict, List
from typing import Any
from .contracts import (
    CartRequest,
    CartResponse,
    Item,
    ItemInfo
)
router = APIRouter()
@router.get(
    "/cart"
)
async def get_cart_list(
    offset: Annotated[NonNegativeInt, Query()] = 0,
    limit: Optional[int] = Query(10, gt=0),
    min_price: Annotated[PositiveFloat, Query()] = None,
    max_price: Annotated[PositiveFloat, Query()] = None,
    min_quantity: Annotated[NonNegativeInt, Query()] = None,
    max_quantity: Annotated[NonNegativeInt, Query()] = None
) -> list[CartResponse]:
    try:
        return [
            CartResponse.from_entity(e) for e in store.get_many_cart(offset,
                                                            limit,
                                                            min_price,
                                                            max_price,
                                                            min_quantity,
                                                            max_quantity)
        ]
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))


@router.get("/item")
async def get_item_list(
    offset: Annotated[NonNegativeInt, Query()] = 0,
    limit: Annotated[PositiveInt, Query()] = 10,
    min_price: Annotated[PositiveFloat, Query()] = None,
    max_price: Annotated[PositiveFloat, Query()] = None,
) -> list[Item]:
    try:
        return store.get_many_item(offset,
                                        limit,
                                        min_price,
                                        max_price)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))


@router.get(
    "/item/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned requested item",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return requested item as one was not found",
        },
    },
)
async def get_item_by_id(id: int) -> Item:
    item = store.get_one_item(id)

    if not item:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /item/{id} was not found",
        )

    return item


@router.delete(
    "/item/{id}"
)
async def delete_item_by_id(id: int):
    item = store.get_one_item(id)

    if not item or item.deleted is True:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /item/{id} was not found",
        )
    store.delete_item(id)


@router.post("/cart/{cart_id}/add/{item_id}")
async def add_item_to_cart(cart_id, item_id):
    entity = store.get_one_cart(cart_id)
    item = store.get_one_item(item_id)

    if not entity:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /cart/{cart_id} was not found",
        )

    if not item:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /item/{item_id} was not found",
        )

    store.add_item_to_cart(cart_id, item_id)


@router.get(
    "/cart/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned requested cart",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return requested cart as one was not found",
        },
    },
)
async def get_cart_by_id(id: int) -> CartResponse:
    entity = store.get_one_cart(id)

    if not entity:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /cart/{id} was not found",
        )

    return CartResponse.from_entity(entity)

@router.post(
    "/cart",
    status_code=HTTPStatus.CREATED
)
async def post_cart(info: CartRequest, response: Response) -> CartResponse:
    entity = store.add_cart(info.as_cart_info())

    response.headers["location"] = f"/cart/{entity.id}"
    return CartResponse.from_entity(entity)


@router.post(
    "/item",
    status_code=HTTPStatus.CREATED
)
async def post_item(info: dict, response: Response) -> Item:
    item = store.add_item(info)

    response.headers["location"] = f"/item/{item.id}"
    return item

@router.put(
    "/item/{id}",
    status_code=HTTPStatus.OK
)
async def put_item(id: int, body) -> Item:
    item = store.get_one_item(id)

    if not item:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /item/{id} was not found",
        )

    store.put_item(id, body)
    return store.get_one_item(id)

@router.patch(
    "/item/{id}",
    status_code=HTTPStatus.OK
)
async def patch_item(id: int, body: dict) -> Item:
    item = store.get_one_item(id)
    if item is None:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /item/{id} was not found",
        )
    if item.deleted:
        raise HTTPException(status_code=HTTPStatus.NOT_MODIFIED)
    try:
        result = store.patch_item(id, body)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))

    return result

