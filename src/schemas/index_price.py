from pydantic import BaseModel


class IndexPriceSchemaGet(BaseModel):
    ticker: str
    price: float
    timestamp: int
