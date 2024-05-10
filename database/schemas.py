from pydantic import BaseModel


class GameBase(BaseModel):
    title: str
    cover: str | None = None
    description: str | None = None
    torrent_file: str
    language: str | None = None
    version: str | None = None
    download_size: str | None = None
    upload_date: str | None = None

    system: str | None = None
    processor: str | None = None
    memory: str | None = None
    graphics: str | None = None
    storage: str | None = None


class GameCreate(GameBase):
    pass


class Game(GameBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str
    name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    games: list[Game] = []

    class Config:
        from_attributes = True
