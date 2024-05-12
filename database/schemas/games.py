from typing import Optional
from pydantic import BaseModel


class GameCardBase(BaseModel):
    title: str
    cover: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None


class GameCard(GameCardBase):
    id: int


class GameBase(GameCardBase):
    torrent_file: str
    trailer: Optional[str] = None

    system: Optional[str] = None
    processor: Optional[str] = None
    memory: Optional[str] = None
    graphics: Optional[str] = None
    storage: Optional[str] = None

    developer: Optional[str] = None
    language: Optional[str] = None
    release_date: Optional[str] = None
    download_size: Optional[str] = None



class GameCreate(GameBase):
    pass


class Game(GameBase):
    id: int
    update_date: str
    upload_date: str
    owner_id: int

    class Config:
        from_attributes = True
