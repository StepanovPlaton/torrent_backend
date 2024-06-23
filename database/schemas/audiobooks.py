from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from .users import UserOpenData as User
from .audiobook_genres import AudiobookGenre


class AudiobookCardBase(BaseModel):
    title: str = Field(examples=["Марсианин"])
    cover: Optional[str] = \
        Field(default=None, examples=["cover_filename.jpg"])
    description: Optional[str] = \
        Field(default=None,
              examples=["Главный герой оказался в сложнейшей ситуации."
                        " Его жизнь висела на волоске и зависела от"
                        " нескольких совершенно нелогичных факторов."
                        " Дело в том, что его бросили на Марсе в крайне"
                        " затруднительном для дальнейшей жизни положении."
                        " Рассчитывать стоит лишь на себя и на чудо,"
                        " ведь ультрасовременный скафандр оказался прошит"
                        " антенной, а до прибытия следующей экспедиции"
                        " остается целая вечность."])
    author: Optional[str] = \
        Field(default=None, examples=["Вейр Энди"])


class AudiobookCard(AudiobookCardBase):
    id: int = Field(examples=[1])


class AudiobookBase(AudiobookCardBase):
    torrent_file: str = Field(examples=["torrent_filename.torrent"])
    fragment: Optional[str] = \
        Field(default=None, examples=[
              "fragment.mp3"])

    language: Optional[str] = Field(default=None, examples=["рус"])
    release_date: Optional[str] = Field(default=None, examples=["2015"])
    download_size: Optional[str] = Field(default=None, examples=["300Mb"])
    duration: Optional[str] = Field(default=None, examples=["12:38"])
    reader: Optional[str] = Field(default=None, examples=["Дмитрий Хазанович"])


class AudiobookCreate(AudiobookBase):
    genres: Optional[list[int]] = Field(default=None, examples=[[1, 2]])


class Audiobook(AudiobookBase):
    id: int = Field(examples=[1])
    update_date: str = Field(examples=["2024-06-14 12:00:00"])

    genres: list[AudiobookGenre] = Field()

    owner: User = Field()

    model_config = ConfigDict(from_attributes=True)
