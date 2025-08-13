from src.entrypoints.routers.items import items_router
from src.entrypoints.routers.management import management_router


def add_routes(app) -> None:
    app.include_router(management_router)
    app.include_router(items_router)
