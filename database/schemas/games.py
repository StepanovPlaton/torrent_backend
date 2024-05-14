from typing import Optional
from fastapi import Body
from pydantic import BaseModel, ConfigDict, Field


class GameCardBase(BaseModel):
    title: str = Field(examples=["DwarfFortress", "RimWorld"])
    cover: Optional[str] = \
        Field(default=None, examples=["cover_filename.jpg"])
    description: Optional[str] = \
        Field(default=None,
              examples=["Dwarf Fortress - это игра, которая"
                        " находится в стадии разработки уже"
                        " довольно долгое время, но уже собрала"
                        " большую базу поклонников и довольно хорошие отзывы"])
    version: Optional[str] = \
        Field(default=None, examples=["50.08 (Steam edition)"])


class GameCard(GameCardBase):
    id: int = Field(examples=[1])


class GameBase(GameCardBase):
    torrent_file: str = Field(examples=["torrent_filename.torrent"])
    trailer: Optional[str] = \
        Field(default=None, examples=[
              "https://www.youtube.com/watch?v=xawsp16oxb0"])

    system: Optional[str] = Field(default=None, examples=["Windows"])
    processor: Optional[str] = \
        Field(default=None, examples=["Любой (от 2Ghz)"])
    memory: Optional[str] = Field(default=None, examples=["512Mb"])
    graphics: Optional[str] = Field(default=None, examples=["Любая"])
    storage: Optional[str] = Field(default=None, examples=["100Mb"])

    developer: Optional[str] = Field(default=None, examples=["Bay12Games"])
    language: Optional[str] = Field(default=None, examples=["eng/рус"])
    release_date: Optional[str] = Field(default=None, examples=["2014"])
    download_size: Optional[str] = Field(default=None, examples=["80Mb"])


class GameCreate(GameBase):
    pass


class Game(GameBase):
    id: int = Field(examples=[1])
    update_date: str = Field(examples=["2024-05-13 12:00:00"])
    upload_date: str = Field(examples=["2024-05-13 12:00:00"])
    owner_id: int = Field(examples=[1])

    model_config = ConfigDict(from_attributes=True)
