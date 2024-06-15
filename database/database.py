from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from env import Env

DATABASE_URL = Env.get_strict("SQLALCHEMY_DATABASE_URL", str)
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_async_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # , echo=True
)
async_session = sessionmaker(  # type: ignore
    engine, class_=AsyncSession, expire_on_commit=False)  # type: ignore
Base = declarative_base()


async def get_session() -> AsyncSession:  # type: ignore
    async with async_session() as session:  # type: ignore
        yield session                       # type: ignore


async def drop_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def recreate_all():
    await drop_all()
    await create_all()


async def add_transaction[T](db: AsyncSession, entity: T) -> T:
    try:
        db.add(entity)
        await db.commit()
        await db.refresh(entity)
        return entity
    except Exception as ex:
        await db.rollback()
        raise ex
