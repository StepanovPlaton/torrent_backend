from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

import database as db
from file_handler import *
from routes.auth import get_user

audiobooks_router = APIRouter(prefix="/audiobooks", tags=["Audiobooks"])


@audiobooks_router.get("", response_model=list[db.Audiobook])
async def get_audiobooks(db_session: AsyncSession = Depends(db.get_session)):
    return await db.get_audiobooks(db_session)


@audiobooks_router.post("", response_model=db.Audiobook)
async def add_audiobook(audiobook: db.AudiobookCreate,
                        user: db.User = Depends(get_user),
                        db_session: AsyncSession = Depends(db.get_session)):
    return await db.add_audiobook(db_session, audiobook, user.id)


@audiobooks_router.get("/cards", response_model=list[db.AudiobookCard])
async def get_audiobooks_cards(db_session: AsyncSession = Depends(db.get_session)):
    return await db.get_audiobooks(db_session)


@audiobooks_router.get("/{audiobook_id}", response_model=db.Audiobook)
async def get_audiobook(audiobook_id: int, db_session: AsyncSession = Depends(db.get_session)):
    return await db.get_audiobook(db_session, audiobook_id)


@audiobooks_router.put("/{audiobook_id}", response_model=db.Audiobook)
async def edit_audiobook(audiobook_id: int,
                         audiobook: db.AudiobookCreate,
                         user: db.User = Depends(get_user),
                         db_session: AsyncSession = Depends(db.get_session)):
    audiobook_db = await db.get_audiobook(db_session, audiobook_id)
    if (audiobook_db is None):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Audiobook with id={audiobook_id} not found")
    if (user.id != audiobook_db.owner_id):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail=f"Audiobook can only be edited "
                            "by the owner (creator)")
    return await db.edit_audiobook(db_session, audiobook_id, audiobook)


@audiobooks_router.delete("/{audiobook_id}", response_model=db.Audiobook)
async def delete_audiobook(audiobook_id: int,
                           user: db.User = Depends(get_user),
                           db_session: AsyncSession = Depends(db.get_session)):
    audiobook_db = await db.get_audiobook(db_session, audiobook_id)
    if (audiobook_db is None):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Audiobook with id={audiobook_id} not found")
    if (user.id != audiobook_db.owner_id):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail=f"Audiobook can only be deleted "
                            "by the owner (creator)")
    return await db.delete_audiobook(db_session, audiobook_id)
