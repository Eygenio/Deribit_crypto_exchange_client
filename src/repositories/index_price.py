from src.models.index_price import IndexPriceOrm
from src.repositories.base import SQLAlchemyRepository


class IndexPriceRepository(SQLAlchemyRepository):
    model = IndexPriceOrm
