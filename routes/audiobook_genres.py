from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from database import *

from file_handler import *
from routes.auth import get_user

audiobook_genres_router = APIRouter(
    prefix="/genres/audiobooks", tags=["Audiobooks", "Genres"])


@audiobook_genres_router.get("", response_model=list[AudiobookGenre])
async def get_audiobook_genres(db_session: AsyncSession = Depends(Database.get_session)):
    return await AudiobookGenresCRUD.get_all(db_session)


@audiobook_genres_router.post("", response_model=AudiobookGenre)
async def add_audiobook_genre(genre: AudiobookGenreCreate,
                              user: User = Depends(get_user),
                              db_session: AsyncSession = Depends(Database.get_session)):
    return await AudiobookGenresCRUD.add(db_session, genre)
