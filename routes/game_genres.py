from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from database import *

from file_handler import *
from routes.auth import get_user

game_genres_router = APIRouter(
    prefix="/genres/games", tags=["Games", "Genres"])


@game_genres_router.get("", response_model=list[GameGenre])
async def get_game_genres(db_session: AsyncSession = Depends(Database.get_session)):
    return await GameGenresCRUD.get_all(db_session)


@game_genres_router.post("", response_model=GameGenre)
async def add_game_genre(genre: GameGenreCreate,
                         user: User = Depends(get_user),
                         db_session: AsyncSession = Depends(Database.get_session)):
    return await GameGenresCRUD.add(db_session, genre)
