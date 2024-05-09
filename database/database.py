from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "sqlite+aiosqlite:///./dev_database.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_async_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def get_session() -> AsyncSession:  # type: ignore
    # Dependency
    async with async_session() as session:  # type: ignore
        yield session


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
