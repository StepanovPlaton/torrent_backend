from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models import *


async def get_user(db: AsyncSession, user_id: int):
    return await db.get(User, user_id)
