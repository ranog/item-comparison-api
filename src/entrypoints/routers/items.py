from fastapi import APIRouter

from src.entrypoints.handlers.items import (
    create_item,
    delete_item,
    get_item,
    list_items,
    replace_item,
    update_item,
)
from src.entrypoints.handlers.comparison import compare_items

items_router = APIRouter(tags=["item-comparison"])

PATH_ITEM_ID = "/items/{item_id}"

items_router.add_api_route(
    "/items",
    list_items,
    methods=["GET"],
)

items_router.add_api_route(
    PATH_ITEM_ID,
    get_item,
    methods=["GET"],
)

items_router.add_api_route(
    "/items",
    create_item,
    methods=["POST"],
    status_code=201,
)

items_router.add_api_route(
    PATH_ITEM_ID,
    replace_item,
    methods=["PUT"],
)

items_router.add_api_route(
    PATH_ITEM_ID,
    update_item,
    methods=["PATCH"],
)

items_router.add_api_route(
    PATH_ITEM_ID,
    delete_item,
    methods=["DELETE"],
    status_code=204,
)

items_router.add_api_route(
    "/items/compare",
    compare_items,
    methods=["GET"],
)
