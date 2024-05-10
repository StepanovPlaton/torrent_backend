from fastapi import APIRouter, Depends, HTTPException

from database import *

router = APIRouter(prefix="/games", tags=["Games"])

@router.get("/", response_model=list[Game])
async def get_games(db: AsyncSession = Depends(get_session)):
    try: return await crud.get_games(db)
    except Exception as ex: raise HTTPException(500)

@router.get("/{game_id}", response_model=Game)
async def get_game(game_id: int, db: AsyncSession = Depends(get_session)):
    return await crud.get_game(db, game_id)

@router.post("/", response_model=Game)
async def add_game(game: GameCreate, user_id: int, db:AsyncSession = Depends(get_session)):
    try: return await crud.add_game(db, game, user_id)
    except Exception as ex: raise HTTPException(500)
    