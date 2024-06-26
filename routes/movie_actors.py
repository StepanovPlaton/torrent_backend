from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from database import *

from file_handler import *
from routes.auth import get_user

movie_actors_router = APIRouter(
    prefix="/actors", tags=["Movies", "Actors"])


@movie_actors_router.get("", response_model=list[MovieActor])
async def get_movie_actors(db_session: AsyncSession = Depends(Database.get_session)):
    return await MovieActorsCRUD.get_all(db_session)


@movie_actors_router.post("", response_model=MovieActor)
async def add_movie_actor(actor: MovieActorCreate,
                          user: User = Depends(get_user),
                          db_session: AsyncSession = Depends(Database.get_session)):
    return await MovieActorsCRUD.add(db_session, actor)
