from pydantic import BaseModel


class IndexPriceResponse(BaseModel):
    ticker: str
    price: float
    timestamp: int
