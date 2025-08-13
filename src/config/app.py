from fastapi import FastAPI

from src.entrypoints import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Item Comparison API",
        description="API para comparação de itens com informações detalhadas",
        version="0.1.0",
    )
    
    router.add_routes(app)
    return app
