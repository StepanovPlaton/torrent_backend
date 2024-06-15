from time import strftime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .. import models as mdl
from .. import schemas as sch
from ..database import add_transaction


async def get_movies(db: AsyncSession):
    return (await db.execute(select(mdl.Movie))).scalars().all()


async def get_movie(db: AsyncSession, movie_id: int):
    return await db.get(mdl.Movie, movie_id)


async def add_movie(db: AsyncSession,
                    movie_info: sch.MovieCreate,
                    user_id: int):
    movie = mdl.Movie(**movie_info.model_dump(),
                      update_date=strftime("%Y-%m-%d %H:%M:%S"),
                      upload_date=strftime("%Y-%m-%d %H:%M:%S"),
                      owner_id=user_id)
    return await add_transaction(db, movie)


async def edit_movie(db: AsyncSession,
                     movie_id: int,
                     movie_info: sch.MovieCreate):
    movie = await db.get(mdl.Movie, movie_id)
    for key, value in vars(movie_info).items():
        if (value and value is not None and getattr(movie, key) != value):
            setattr(movie, key, value)
    setattr(movie, "update_date", strftime("%Y-%m-%d %H:%M:%S"))
    await db.commit()
    return movie


async def delete_movie(db: AsyncSession,
                       movie_id: int):
    movie = await get_movie(db, movie_id)
    await db.delete(movie)
    await db.commit()
    return movie
