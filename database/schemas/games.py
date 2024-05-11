from pydantic import BaseModel


class GameCardBase(BaseModel):
    title: str
    cover: str | None = None
    description: str | None = None


class GameCard(GameCardBase):
    id: int
    upload_date: str | None = None


class GameBase(GameCardBase):
    torrent_file: str
    language: str | None = None
    version: str | None = None
    download_size: str | None = None

    system: str | None = None
    processor: str | None = None
    memory: str | None = None
    graphics: str | None = None
    storage: str | None = None


class GameCreate(GameBase):
    pass


class Game(GameBase):
    id: int
    upload_date: str | None
    owner_id: int

    class Config:
        from_attributes = True
