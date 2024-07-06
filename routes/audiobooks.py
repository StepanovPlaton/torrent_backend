from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from database import *
from file_handler import *
from routes.auth import get_user

audiobooks_router = APIRouter(prefix="/audiobooks", tags=["Audiobooks"])


@audiobooks_router.get("/{audiobook_id}", response_model=Audiobook)
async def get_audiobook(audiobook_id: int, db_session: AsyncSession = Depends(Database.get_session)):
    return await AudiobooksCRUD.get(db_session, audiobook_id)


@audiobooks_router.get("", response_model=list[AudiobookCard])
async def get_audiobooks_cards(db_session: AsyncSession = Depends(Database.get_session)):
    return await AudiobooksCRUD.get_all(db_session)


@audiobooks_router.post("", response_model=Audiobook)
async def add_audiobook(audiobook: AudiobookCreate,
                        user: User = Depends(get_user),
                        db_session: AsyncSession = Depends(Database.get_session)):
    return await AudiobooksCRUD.add(db_session, audiobook, user.id)


@audiobooks_router.put("/{audiobook_id}", response_model=Audiobook)
async def edit_audiobook(audiobook_id: int,
                         audiobook: AudiobookCreate,
                         user: User = Depends(get_user),
                         db_session: AsyncSession = Depends(Database.get_session)):
    audiobook_db = await AudiobooksCRUD.get(db_session, audiobook_id)
    if (audiobook_db is None):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Audiobook with id={audiobook_id} not found")
    if (user.id != audiobook_db.owner_id):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail=f"Audiobook can only be edited "
                            "by the owner (creator)")
    return await AudiobooksCRUD.change(db_session, audiobook_id, audiobook)


@audiobooks_router.delete("/{audiobook_id}", response_model=Audiobook)
async def delete_audiobook(audiobook_id: int,
                           user: User = Depends(get_user),
                           db_session: AsyncSession = Depends(Database.get_session)):
    audiobook_db = await AudiobooksCRUD.get(db_session, audiobook_id)
    if (audiobook_db is None):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Audiobook with id={audiobook_id} not found")
    if (user.id != audiobook_db.owner_id):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail=f"Audiobook can only be deleted "
                            "by the owner (creator)")
    return await AudiobooksCRUD.delete(db_session, audiobook_id)
