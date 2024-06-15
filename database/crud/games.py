from time import strftime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .. import models as mdl
from .. import schemas as sch
from ..database import add_transaction


async def get_games(db: AsyncSession):
    return (await db.execute(select(mdl.Game))).scalars().all()


async def get_game(db: AsyncSession, game_id: int):
    return await db.get(mdl.Game, game_id)


async def add_game(db: AsyncSession,
                   game_info: sch.GameCreate,
                   user_id: int):
    game = mdl.Game(**game_info.model_dump(),
                    update_date=strftime("%Y-%m-%d %H:%M:%S"),
                    upload_date=strftime("%Y-%m-%d %H:%M:%S"),
                    owner_id=user_id)
    return await add_transaction(db, game)


async def edit_game(db: AsyncSession,
                    game_id: int,
                    game_info: sch.GameCreate):
    game = await db.get(mdl.Game, game_id)
    for key, value in vars(game_info).items():
        if (value and value is not None and getattr(game, key) != value):
            setattr(game, key, value)
    setattr(game, "update_date", strftime("%Y-%m-%d %H:%M:%S"))
    await db.commit()
    return game


async def delete_game(db: AsyncSession,
                      game_id: int):
    game = await get_game(db, game_id)
    await db.delete(game)
    await db.commit()
    return game
