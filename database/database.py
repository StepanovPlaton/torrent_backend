from abc import ABC, abstractmethod
from time import strftime
from typing import Any, Callable, Coroutine, Generic, Type
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
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


class Database:
    @staticmethod
    async def get_session() -> AsyncSession:  # type: ignore
        async with async_session() as session:  # type: ignore
            yield session                       # type: ignore

    @staticmethod
    async def drop_all():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @staticmethod
    async def create_all():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def recreate_all():
        await Database.drop_all()
        await Database.create_all()

    @staticmethod
    async def get[T](db: AsyncSession, typeof_entity: Type[T], entity_id: int) -> T | None:
        return await db.get(typeof_entity, entity_id)

    @staticmethod
    async def get_all[T](db: AsyncSession, typeof_entity: Type[T]) -> list[T]:
        return list((await db.execute(select(typeof_entity))).scalars().all())

    @staticmethod
    async def add[T](db: AsyncSession, entity: T) -> T:
        try:
            db.add(entity)
            await db.commit()
            await db.refresh(entity)
            return entity
        except Exception as ex:
            await db.rollback()
            raise ex

    @staticmethod
    async def change[T, U](db: AsyncSession, typeof_entity: Type[T],
                           entity_id: int, info: U,
                           additional_change: Callable[[AsyncSession, T, U], Coroutine[Any, Any, None]] | None = None) -> T:
        try:
            entity = await db.get(typeof_entity, entity_id)
            if (entity is None):
                raise ValueError(f"Can't change entity. " +
                                 f"{str(typeof_entity)} with id={entity_id} not found")
            for key, value in vars(info).items():
                try:
                    if (getattr(entity, key) != value):
                        setattr(entity, key, value)
                except:
                    ...
            setattr(entity, "update_date", strftime("%Y-%m-%d %H:%M:%S"))
            if (additional_change):
                await additional_change(db, entity, info)
            await db.commit()
            return entity
        except Exception as ex:
            await db.rollback()
            raise ex

    @staticmethod
    async def delete[T](db: AsyncSession, typeof_entity: Type[T], entity_id: int) -> T:
        try:
            entity = await db.get(typeof_entity, entity_id)
            if (entity is None):
                raise ValueError(f"Can't delete entity. " +
                                 f"{str(typeof_entity)} with id={entity_id} not found")
            await db.delete(entity)
            await db.commit()
            return entity
        except Exception as ex:
            await db.rollback()
            raise ex


class EntityCRUD[T](ABC):
    @staticmethod
    @abstractmethod
    async def get(db: AsyncSession, id: int) -> T | None: ...

    @staticmethod
    @abstractmethod
    async def get_all(db: AsyncSession) -> list[T]: ...

    @staticmethod
    @abstractmethod
    async def add(db: AsyncSession, entity: T,
                  owner_id: int | None = None) -> T: ...

    @staticmethod
    @abstractmethod
    async def change(db: AsyncSession, entity_id: int, info: object) -> T: ...

    @staticmethod
    @abstractmethod
    async def delete(db: AsyncSession, entity_id: int) -> T: ...
