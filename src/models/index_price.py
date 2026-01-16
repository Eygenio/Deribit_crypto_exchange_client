from sqlalchemy import String, BigInteger, Index
from sqlalchemy.orm import Mapped, mapped_column

import time

from src.models.base import ModelBase


class IndexPriceOrm(ModelBase):
    __tablename__ = "index_price"

    __table_args__ = (Index("idx_ticker_timestamp", "ticker", "timestamp"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] = mapped_column(String(20), index=True)
    price: Mapped[float]
    timestamp: Mapped[int] = mapped_column(
        BigInteger,
        default=lambda: int(time.time()),
        index=True
    )
