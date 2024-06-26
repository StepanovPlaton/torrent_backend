from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from database import *

from file_handler import *
from routes.auth import get_user

movie_genres_router = APIRouter(
    prefix="/genres/movies", tags=["Movies", "Genres"])


@movie_genres_router.get("", response_model=list[MovieGenre])
async def get_movie_genres(db_session: AsyncSession = Depends(Database.get_session)):
    return await MovieGenresCRUD.get_all(db_session)


@movie_genres_router.post("", response_model=MovieGenre)
async def add_movie_genre(genre: MovieGenreCreate,
                          user: User = Depends(get_user),
                          db_session: AsyncSession = Depends(Database.get_session)):
    return await MovieGenresCRUD.add(db_session, genre)
