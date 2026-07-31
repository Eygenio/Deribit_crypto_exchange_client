import logging.config
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.config.logging_config import LOGGING_CONFIG
from src.db.db import create_tables
from src.presentation.api.prices import router as prices_router

logging.config.dictConfig(LOGGING_CONFIG)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    await create_tables()
    yield


app = FastAPI(
    title="Crypto Price API",
    version="1.0.0",
    description="Public API v1",
    lifespan=lifespan,
)

app.include_router(prices_router)


if __name__ == "__main__":
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=True)
