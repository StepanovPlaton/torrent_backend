from pydantic import BaseModel, ConfigDict, Field


class MovieActorBase(BaseModel):
    actor: str = Field(default=None, examples=["Мэттью Макконахи"])


class MovieActorCreate(MovieActorBase):
    pass


class MovieActor(MovieActorBase):
    id: int = Field(examples=[1])

    model_config = ConfigDict(from_attributes=True)
