from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

import database as db
from file_handler import *
from routes.auth import get_user

games_router = APIRouter(prefix="/games", tags=["Games"])


@games_router.get("", response_model=list[db.Game])
async def get_games(db_session: AsyncSession = Depends(db.get_session)):
    return await db.get_games(db_session)


@games_router.post("", response_model=db.Game)
async def add_game(game: db.GameCreate,
                   user: db.User = Depends(get_user),
                   db_session: AsyncSession = Depends(db.get_session)):
    return await db.add_game(db_session, game, user.id)


@games_router.get("/cards", response_model=list[db.GameCard])
async def get_games_cards(db_session: AsyncSession = Depends(db.get_session)):
    return await db.get_games(db_session)


@games_router.get("/{game_id}", response_model=db.Game)
async def get_game(game_id: int, db_session: AsyncSession = Depends(db.get_session)):
    return await db.get_game(db_session, game_id)


@games_router.put("/{game_id}", response_model=db.Game)
async def edit_game(game_id: int,
                    game: db.GameCreate,
                    user: db.User = Depends(get_user),
                    db_session: AsyncSession = Depends(db.get_session)):
    game_db = await db.get_game(db_session, game_id)
    if (game_db is None):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Game with id={game_id} not found")
    if (user.id != game_db.owner_id):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail=f"Game can only be edited "
                            "by the owner (creator)")
    return await db.edit_game(db_session, game_id, game)


@games_router.delete("/{game_id}", response_model=db.Game)
async def delete_game(game_id: int,
                      user: db.User = Depends(get_user),
                      db_session: AsyncSession = Depends(db.get_session)):
    game_db = await db.get_game(db_session, game_id)
    if (game_db is None):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Game with id={game_id} not found")
    if (user.id != game_db.owner_id):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail=f"Game can only be deleted "
                            "by the owner (creator)")
    return await db.delete_game(db_session, game_id)
