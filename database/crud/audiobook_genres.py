from time import strftime
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import Database, EntityCRUD

from .. import models as mdl
from .. import schemas as sch


class AudiobookGenresCRUD(EntityCRUD[mdl.AudiobookGenre]):
    @staticmethod
    async def get_all(db: AsyncSession):
        return await Database.get_all(db, mdl.AudiobookGenre)

    @staticmethod
    async def add(db: AsyncSession,
                  info: sch.AudiobookGenreCreate):
        audiobook_genre = mdl.AudiobookGenre(**info.model_dump())
        return await Database.add(db, audiobook_genre)
