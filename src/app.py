from fastapi import FastAPI

from src.routing.index_price import router
from src.db.db import create_tables


app = FastAPI(
    title="Crypto Price API",
    version="1.0.0",
    description="Public API v1"
)

@app.on_event("startup")
async def startup():
    await create_tables()


app.include_router(router)
