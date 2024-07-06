from time import strftime
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud.movie_actors import MovieActorsCRUD
from database.crud.movie_genres import MovieGenresCRUD
from database.database import Database, EntityCRUD

from .. import models as mdl
from .. import schemas as sch


class MoviesCRUD(EntityCRUD[mdl.Movie]):
    @staticmethod
    async def get(db: AsyncSession, id: int):
        return await Database.get(db, mdl.Movie, id)

    @staticmethod
    async def get_all(db: AsyncSession):
        return await Database.get_all(db, mdl.Movie)

    @staticmethod
    async def change_actors(db: AsyncSession, movie: mdl.Movie, info: sch.MovieCreate):
        movie_actors = await MovieActorsCRUD.get_all(db)
        if (info.actors):
            actors_id = [actor.id for actor in info.actors]
            movie.actors = [
                actor for actor in movie_actors if actor.id in actors_id]

    @staticmethod
    async def change_genres(db: AsyncSession, movie: mdl.Movie, info: sch.MovieCreate):
        movie_genres = await MovieGenresCRUD.get_all(db)
        if (info.genres):
            genres_id = [genre.id for genre in info.genres]
            movie.genres = [
                genre for genre in movie_genres if genre.id in genres_id]

    @staticmethod
    async def add(db: AsyncSession,
                  info: sch.MovieCreate,
                  owner_id: int):
        movie_data_db = \
            {k: v for k, v in info.model_dump().items()
             if not k in ["actors", "genres", "update_date"]}
        movie = mdl.Movie(**movie_data_db,
                          update_date=strftime("%Y-%m-%d %H:%M:%S"),
                          owner_id=owner_id)
        await MoviesCRUD.change_genres(db, movie, info)
        await MoviesCRUD.change_actors(db, movie, info)
        return await Database.add(db, movie)

    @staticmethod
    async def change(db: AsyncSession,
                     id: int,
                     info: sch.MovieCreate):
        async def additional_change(db: AsyncSession, movie: mdl.Movie, info: sch.MovieCreate):
            await MoviesCRUD.change_genres(db, movie, info)
            await MoviesCRUD.change_actors(db, movie, info)
        return await Database.change(db, mdl.Movie, id, info, additional_change)

    @staticmethod
    async def delete(db: AsyncSession,
                     id: int):
        return await Database.delete(db, mdl.Movie, id)
