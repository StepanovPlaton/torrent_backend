from time import strftime
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import Database, EntityCRUD

from .. import models as mdl
from .. import schemas as sch


class MovieGenresCRUD(EntityCRUD[mdl.MovieGenre]):
    @staticmethod
    async def get_all(db: AsyncSession):
        return await Database.get_all(db, mdl.MovieGenre)

    @staticmethod
    async def add(db: AsyncSession,
                  info: sch.MovieGenreCreate):
        movie_genre = mdl.MovieGenre(**info.model_dump())
        return await Database.add(db, movie_genre)
