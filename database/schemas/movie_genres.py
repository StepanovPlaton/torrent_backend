from pydantic import BaseModel, ConfigDict, Field


class MovieGenreBase(BaseModel):
    genre: str = Field(default=None, examples=["Фантастика"])


class MovieGenreCreate(MovieGenreBase):
    pass


class MovieGenre(MovieGenreBase):
    id: int = Field(examples=[1])

    model_config = ConfigDict(from_attributes=True)
