from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .. import models as mdl
from .. import schemas as sch
from ..database import add_transaction


async def get_user(db: AsyncSession, username: str):
    return (await db.execute(select(mdl.User).where(mdl.User.name == username))).scalar()


async def add_user(db: AsyncSession,
                   user_data: sch.UserCreate, hash_of_password: str):
    user_data_db = \
        {k: v for k, v in user_data.model_dump().items()
         if k != "password"}
    user = mdl.User(**user_data_db,
                    hash_of_password=hash_of_password)
    return await add_transaction(db, user)


async def check_email(db: AsyncSession, email: str):
    users = (await db.execute(select(mdl.User)
                              .where(mdl.User.email == email))).scalars().all()
    return True if len(users) == 0 else False
