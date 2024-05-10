from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .. import models as mdl
from .. import schemas as sch
from ..database import add_transaction

async def add_game(db: AsyncSession, 
                   game_info: sch.GameCreate, 
                   user_id: int):
    game = mdl.Game(**game_info.model_dump(), owner_id=user_id)
    return await add_transaction(db, game)

async def get_games(db: AsyncSession):
    return (await db.execute(select(mdl.Game))).scalars().all()

async def get_game(db: AsyncSession, game_id: int):
    return await db.get(mdl.Game, game_id)