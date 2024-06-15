from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


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
    pass


class Movie(MovieBase):
    id: int = Field(examples=[1])
    update_date: str = Field(examples=["2024-06-11 12:00:00"])
    upload_date: str = Field(examples=["2024-06-11 12:00:00"])
    owner_id: int = Field(examples=[1])

    model_config = ConfigDict(from_attributes=True)
