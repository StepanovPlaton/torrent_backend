from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from .users import UserOpenData as User
from .movie_genres import MovieGenre
from .movie_actors import MovieActor


class MovieCardBase(BaseModel):
    title: str = Field(examples=["Интерстеллар"])
    cover: Optional[str] = \
        Field(default=None, examples=["cover_filename.jpg"])
    description: Optional[str] = \
        Field(default=None,
              examples=["Когда засуха, пыльные бури и вымирание"
                        " растений приводят человечество к"
                        " продовольственному кризису, коллектив"
                        " исследователей и учёных отправляется"
                        " сквозь червоточину (которая предположительно"
                        " соединяет области пространства-времени"
                        " через большое расстояние) в путешествие,"
                        " чтобы превзойти прежние ограничения для"
                        " космических путешествий человека и найти"
                        " планету с подходящими для человечества условиями."])
    age: Optional[str] = \
        Field(default=None, examples=["18+"])


class MovieCard(MovieCardBase):
    id: int = Field(examples=[1])


class MovieBase(MovieCardBase):
    torrent_file: str = Field(examples=["torrent_filename.torrent"])
    trailer: Optional[str] = \
        Field(default=None, examples=[
              "https://www.youtube.com/watch?v=6ybBuTETr3U"])

    language: Optional[str] = Field(default=None, examples=["рус"])
    subtitles: Optional[str] = Field(default=None, examples=["Отсутствуют"])
    release_date: Optional[str] = Field(default=None, examples=["2014"])
    download_size: Optional[str] = Field(default=None, examples=["32Gb"])
    director: Optional[str] = Field(default=None, examples=["Кристофер Нолан"])
    duration: Optional[str] = Field(default=None, examples=["02:37:58"])
    country: Optional[str] = \
        Field(default=None, examples=["США, Великобритания, Канада"])


class MovieCreate(MovieBase):
    genres: Optional[list[int]] = Field(default=None, examples=[[1, 2]])
    actors: Optional[list[int]] = Field(default=None, examples=[[1, 2]])


class Movie(MovieBase):
    id: int = Field(examples=[1])
    update_date: str = Field(examples=["2024-06-11 12:00:00"])

    genres: list[MovieGenre] = Field()
    actors: list[MovieActor] = Field()

    owner: User = Field()

    model_config = ConfigDict(from_attributes=True)
