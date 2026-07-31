from sqlalchemy import BigInteger, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.models.base import ModelBase


class IndexPriceOrm(ModelBase):
    __tablename__ = "index_price"

    __table_args__ = (Index("idx_ticker_timestamp", "ticker", "timestamp"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] = mapped_column(String(20))
    price: Mapped[float]
    timestamp: Mapped[int] = mapped_column(BigInteger, index=True)
