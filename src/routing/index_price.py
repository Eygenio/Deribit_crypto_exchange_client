from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_async_session
from src.repositories.index_price import IndexPriceRepository
from src.services.index_price import IndexPriceService
from src.schemas.index_price import IndexPriceSchemaGet

router = APIRouter()

def get_service(session: AsyncSession = Depends(get_async_session)):
    return IndexPriceService(IndexPriceRepository(session))

@router.get("/api/prices",
            response_model=List[IndexPriceSchemaGet],
            tags=["Index Price"],
            summary="Получение всех записей.",
            description="Возвращает список всех записей по ticker,"
                        "возможно задавать параметры пагинации."
            )
async def get_all(
        ticker: str = Query(...),
        page: int = Query(1, ge=1),
        service=Depends(get_service)
):
    return await service.get_all(ticker.lower(), page)

@router.get("/api/price/last",
            response_model=IndexPriceSchemaGet | None,
            tags=["Index Price"],
            summary="Получение последней записи.",
            description="Возвращает последнюю запись по ticker."
            )
async def get_last(
        ticker: str = Query(...),
        service=Depends(get_service)
):
    return await service.get_last(ticker.lower())

@router.get("/api/price/by-date",
            response_model=List[IndexPriceSchemaGet],
            tags=["Index Price"],
            summary="Получение записей с фильтром по дате.",
            description="Возвращает список записей по ticket,"
                        "с параметрами от даты до даты,"
                        "возможно задавать  параметры пагинации."
            )
async def get_by_date(
        ticker: str = Query(...),
        from_ts: int = Query(...),
        to_ts: int = Query(...),
        page: int = Query(1),
        service=Depends(get_service)
):
    return await service.get_by_date(ticker.lower(), from_ts, to_ts, page)
