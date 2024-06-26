from time import strftime
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import Database, EntityCRUD

from .. import models as mdl
from .. import schemas as sch


class MovieActorsCRUD(EntityCRUD[mdl.MovieActor]):
    @staticmethod
    async def get_all(db: AsyncSession):
        return await Database.get_all(db, mdl.MovieActor)

    @staticmethod
    async def add(db: AsyncSession,
                  info: sch.MovieActorCreate):
        movie_actor = mdl.MovieActor(**info.model_dump())
        return await Database.add(db, movie_actor)
