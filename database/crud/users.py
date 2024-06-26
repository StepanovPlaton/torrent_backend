from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.database import Database, EntityCRUD

from .. import models as mdl
from .. import schemas as sch


class UsersCRUD(EntityCRUD[mdl.User]):
    @staticmethod
    async def get(db: AsyncSession, username: str):
        return (await db.execute(select(mdl.User).where(mdl.User.name == username))).scalar()

    @staticmethod
    async def get_all(db: AsyncSession):
        return await Database.get_all(db, mdl.User)

    @staticmethod
    async def add(db: AsyncSession,
                  info: sch.UserCreate,
                  hash_of_password: str):
        user_data_db = \
            {k: v for k, v in info.model_dump().items()
             if k != "password"}
        user = mdl.User(**user_data_db,
                        hash_of_password=hash_of_password)
        return await Database.add(db, user)

    @staticmethod
    async def change(db: AsyncSession,
                     id: int,
                     info: sch.UserCreate):
        return await Database.change(db, mdl.User, id, info)

    @staticmethod
    async def delete_user(db: AsyncSession,
                          id: int):
        return await Database.delete(db, mdl.User, id)

    @staticmethod
    async def check_email(db: AsyncSession, email: str):
        users = (await db.execute(select(mdl.User)
                                  .where(mdl.User.email == email))).scalars().all()
        return True if len(users) == 0 else False
