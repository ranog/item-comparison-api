from fastapi import FastAPI

from src.entrypoints import router


def create_app() -> FastAPI:
    app = FastAPI()
    router.add_routes(app)
    return app
