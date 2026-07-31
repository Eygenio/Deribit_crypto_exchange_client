from pydantic import BaseModel


class IndexPrice(BaseModel):
    id: int | None = None
    ticker: str
    price: float
    timestamp: int
