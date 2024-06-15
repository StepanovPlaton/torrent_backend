from time import strftime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .. import models as mdl
from .. import schemas as sch
from ..database import add_transaction


async def get_audiobooks(db: AsyncSession):
    return (await db.execute(select(mdl.Audiobook))).scalars().all()


async def get_audiobook(db: AsyncSession, audiobook_id: int):
    return await db.get(mdl.Audiobook, audiobook_id)


async def add_audiobook(db: AsyncSession,
                        audiobook_info: sch.AudiobookCreate,
                        user_id: int):
    audiobook = mdl.Audiobook(**audiobook_info.model_dump(),
                              update_date=strftime("%Y-%m-%d %H:%M:%S"),
                              upload_date=strftime("%Y-%m-%d %H:%M:%S"),
                              owner_id=user_id)
    return await add_transaction(db, audiobook)


async def edit_audiobook(db: AsyncSession,
                         audiobook_id: int,
                         audiobook_info: sch.AudiobookCreate):
    audiobook = await db.get(mdl.Audiobook, audiobook_id)
    for key, value in vars(audiobook_info).items():
        if (value and value is not None and getattr(audiobook, key) != value):
            setattr(audiobook, key, value)
    setattr(audiobook, "update_date", strftime("%Y-%m-%d %H:%M:%S"))
    await db.commit()
    return audiobook


async def delete_audiobook(db: AsyncSession,
                           audiobook_id: int):
    audiobook = await get_audiobook(db, audiobook_id)
    await db.delete(audiobook)
    await db.commit()
    return audiobook
