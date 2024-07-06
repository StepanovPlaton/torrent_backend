from time import strftime
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud.game_genres import GameGenresCRUD
from database.database import Database, EntityCRUD

from .. import models as mdl
from .. import schemas as sch


class GamesCRUD(EntityCRUD[mdl.Game]):
    @staticmethod
    async def get(db: AsyncSession, id: int):
        return await Database.get(db, mdl.Game, id)

    @staticmethod
    async def get_all(db: AsyncSession):
        return await Database.get_all(db, mdl.Game)

    @staticmethod
    async def change_genres(db: AsyncSession, game: mdl.Game, info: sch.GameCreate):
        game_genres = await GameGenresCRUD.get_all(db)
        if (info.genres):
            genres_id = [genre.id for genre in info.genres]
            game.genres = [
                genre for genre in game_genres if genre.id in genres_id]

    @staticmethod
    async def add(db: AsyncSession,
                  info: sch.GameCreate,
                  owner_id: int):
        game_data_db = \
            {k: v for k, v in info.model_dump().items()
             if not k in ["genres", "update_date"]}
        game = mdl.Game(**game_data_db,
                        update_date=strftime("%Y-%m-%d %H:%M:%S"),
                        owner_id=owner_id)
        await GamesCRUD.change_genres(db, game, info)
        return await Database.add(db, game)

    @staticmethod
    async def change(db: AsyncSession,
                     id: int,
                     info: sch.GameCreate):
        return await Database.change(db, mdl.Game, id, info, GamesCRUD.change_genres)

    @staticmethod
    async def delete(db: AsyncSession,
                     id: int):
        return await Database.delete(db, mdl.Game, id)
