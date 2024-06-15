from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

import database as db
from file_handler import *
from routes.auth import get_user

movies_router = APIRouter(prefix="/movies", tags=["Movies"])


@movies_router.get("", response_model=list[db.Movie])
async def get_movies(db_session: AsyncSession = Depends(db.get_session)):
    return await db.get_movies(db_session)


@movies_router.post("", response_model=db.Movie)
async def add_movie(movie: db.MovieCreate,
                    user: db.User = Depends(get_user),
                    db_session: AsyncSession = Depends(db.get_session)):
    return await db.add_movie(db_session, movie, user.id)


@movies_router.get("/cards", response_model=list[db.MovieCard])
async def get_movies_cards(db_session: AsyncSession = Depends(db.get_session)):
    return await db.get_movies(db_session)


@movies_router.get("/{movie_id}", response_model=db.Movie)
async def get_movie(movie_id: int, db_session: AsyncSession = Depends(db.get_session)):
    return await db.get_movie(db_session, movie_id)


@movies_router.put("/{movie_id}", response_model=db.Movie)
async def edit_movie(movie_id: int,
                     movie: db.MovieCreate,
                     user: db.User = Depends(get_user),
                     db_session: AsyncSession = Depends(db.get_session)):
    movie_db = await db.get_movie(db_session, movie_id)
    if (movie_db is None):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Movie with id={movie_id} not found")
    if (user.id != movie_db.owner_id):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail=f"Movie can only be edited "
                            "by the owner (creator)")
    return await db.edit_movie(db_session, movie_id, movie)


@movies_router.delete("/{movie_id}", response_model=db.Movie)
async def delete_movie(movie_id: int,
                       user: db.User = Depends(get_user),
                       db_session: AsyncSession = Depends(db.get_session)):
    movie_db = await db.get_movie(db_session, movie_id)
    if (movie_db is None):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Movie with id={movie_id} not found")
    if (user.id != movie_db.owner_id):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail=f"Movie can only be deleted "
                            "by the owner (creator)")
    return await db.delete_movie(db_session, movie_id)
