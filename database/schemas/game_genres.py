from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class GameGenreBase(BaseModel):
    genre: str = Field(default=None, examples=["Стратегия"])


class GameGenreCreate(GameGenreBase):
    pass


class GameGenre(GameGenreBase):
    id: int = Field(examples=[1])

    model_config = ConfigDict(from_attributes=True)
