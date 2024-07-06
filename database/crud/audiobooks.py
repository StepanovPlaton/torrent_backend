from time import strftime
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud.audiobook_genres import AudiobookGenresCRUD
from database.database import Database, EntityCRUD

from .. import models as mdl
from .. import schemas as sch


class AudiobooksCRUD(EntityCRUD[mdl.Audiobook]):
    @staticmethod
    async def get(db: AsyncSession, id: int):
        return await Database.get(db, mdl.Audiobook, id)

    @staticmethod
    async def get_all(db: AsyncSession):
        return await Database.get_all(db, mdl.Audiobook)

    @staticmethod
    async def change_genres(db: AsyncSession, audiobook: mdl.Audiobook, info: sch.AudiobookCreate):
        audiobook_genres = await AudiobookGenresCRUD.get_all(db)
        if (info.genres):
            genres_id = [genre.id for genre in info.genres]
            audiobook.genres = [
                genre for genre in audiobook_genres if genre.id in genres_id]

    @staticmethod
    async def add(db: AsyncSession,
                  info: sch.AudiobookCreate,
                  owner_id: int):
        audiobook_data_db = \
            {k: v for k, v in info.model_dump().items()
             if not k in ["genres", "update_date"]}
        audiobook = mdl.Audiobook(**audiobook_data_db,
                                  update_date=strftime("%Y-%m-%d %H:%M:%S"),
                                  owner_id=owner_id)
        await AudiobooksCRUD.change_genres(db, audiobook, info)
        return await Database.add(db, audiobook)

    @staticmethod
    async def change(db: AsyncSession,
                     id: int,
                     info: sch.AudiobookCreate):
        return await Database.change(db, mdl.Audiobook, id, info, AudiobooksCRUD.change_genres)

    @staticmethod
    async def delete(db: AsyncSession,
                     id: int):
        return await Database.delete(db, mdl.Audiobook, id)
