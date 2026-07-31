import logging

from fastapi import APIRouter, Depends, Query

from src.application.services.price_service import PriceService
from src.presentation.dependencies import get_price_service
from src.presentation.schemas.price import IndexPriceResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/api/prices", response_model=list[IndexPriceResponse])
async def get_all_prices(
    ticker: str = Query(..., description="Currency pair, e.g. btc_usd"),
    page: int = Query(1, ge=1),
    service: PriceService = Depends(get_price_service),
) -> list[IndexPriceResponse]:
    logger.info("Fetching all prices for %s, page %d", ticker, page)
    result = await service.get_all(ticker.lower(), page)
    return [
        IndexPriceResponse(
            ticker=item.ticker,
            price=item.price,
            timestamp=item.timestamp,
        )
        for item in result
    ]


@router.get("/api/price/last", response_model=IndexPriceResponse | None)
async def get_last_price(
    ticker: str = Query(..., description="Currency pair, e.g. btc_usd"),
    service: PriceService = Depends(get_price_service),
) -> IndexPriceResponse | None:
    logger.info("Fetching last price for %s", ticker)
    result = await service.get_last(ticker.lower())
    if result is None:
        return None
    return IndexPriceResponse(
        ticker=result.ticker,
        price=result.price,
        timestamp=result.timestamp,
    )


@router.get("/api/price/by-date", response_model=list[IndexPriceResponse])
async def get_prices_by_date(
    ticker: str = Query(..., description="Currency pair, e.g. btc_usd"),
    from_ts: int = Query(..., description="From UNIX timestamp"),
    to_ts: int = Query(..., description="To UNIX timestamp"),
    page: int = Query(1, ge=1),
    service: PriceService = Depends(get_price_service),
) -> list[IndexPriceResponse]:
    logger.info("Fetching prices for %s from %d to %d, page %d", ticker, from_ts, to_ts, page)
    result = await service.get_by_date(ticker.lower(), from_ts, to_ts, page)
    return [
        IndexPriceResponse(
            ticker=item.ticker,
            price=item.price,
            timestamp=item.timestamp,
        )
        for item in result
    ]
