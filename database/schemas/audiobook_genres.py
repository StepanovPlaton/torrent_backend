from pydantic import BaseModel, ConfigDict, Field


class AudiobookGenreBase(BaseModel):
    genre: str = Field(default=None, examples=["Боевик"])


class AudiobookGenreCreate(AudiobookGenreBase):
    pass


class AudiobookGenre(AudiobookGenreBase):
    id: int = Field(examples=[1])

    model_config = ConfigDict(from_attributes=True)
