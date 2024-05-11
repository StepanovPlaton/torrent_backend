from fastapi import APIRouter, Depends, HTTPException

from database import *
from file_handler import *

games_router = APIRouter(prefix="/games", tags=["Games"])


@games_router.get("/", response_model=list[Game])
async def get_games(db: AsyncSession = Depends(get_session)):
    try:
        return await crud.get_games(db)
    except Exception:
        raise HTTPException(500)


@games_router.get("/cards", response_model=list[GameCard])
async def get_games_cards(db: AsyncSession = Depends(get_session)):
    try:
        return await crud.get_games(db)
    except Exception:
        raise HTTPException(500)


@games_router.get("/{game_id}", response_model=Game)
async def get_game(game_id: int, db: AsyncSession = Depends(get_session)):
    return await crud.get_game(db, game_id)


@games_router.post("/", response_model=Game)
async def add_game(game: GameCreate,
                   user_id: int,
                   db: AsyncSession = Depends(get_session)):
    try:
        return await crud.add_game(db, game, user_id)
    except Exception:
        raise HTTPException(500)
