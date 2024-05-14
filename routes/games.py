from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

import database as db
from file_handler import *

games_router = APIRouter(prefix="/games", tags=["Games"])


@games_router.get("/", response_model=list[db.Game])
async def get_games(db_session: AsyncSession = Depends(db.get_session)):
    return await db.get_games(db_session)


@games_router.get("/cards", response_model=list[db.GameCard])
async def get_games_cards(db_session: AsyncSession = Depends(db.get_session)):
    return await db.get_games(db_session)


@games_router.get("/{game_id}", response_model=db.Game)
async def get_game(game_id: int, db_session: AsyncSession = Depends(db.get_session)):
    return await db.get_game(db_session, game_id)


@games_router.put("/{game_id}", response_model=db.Game)
async def edit_game(game_id: int,
                    game: db.GameCreate,
                    db_session: AsyncSession = Depends(db.get_session)):
    return await db.edit_game(db_session, game_id, game)


@games_router.post("/", response_model=db.Game)
async def add_game(game: db.GameCreate,
                   user_id: int,
                   db_session: AsyncSession = Depends(db.get_session)):
    return await db.add_game(db_session, game, user_id)
