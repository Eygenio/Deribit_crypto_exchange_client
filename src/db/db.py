import logging
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config.base import Config
from src.models.base import ModelBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_async_engine(Config.DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session():
    async with async_session_maker() as session:
        yield session


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(ModelBase.metadata.create_all)
