from time import strftime
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import Database, EntityCRUD

from .. import models as mdl
from .. import schemas as sch


class GameGenresCRUD(EntityCRUD[mdl.GameGenre]):

    @staticmethod
    async def get_all(db: AsyncSession):
        return await Database.get_all(db, mdl.GameGenre)

    @staticmethod
    async def add(db: AsyncSession,
                  info: sch.GameGenreCreate):
        game_genre = mdl.GameGenre(**info.model_dump())
        return await Database.add(db, game_genre)
