from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)

    title = Column(String, nullable=False, unique=True)
    cover = Column(String)
    age = Column(String)
    description = Column(String)

    torrent_file = Column(String, nullable=False)
    trailer = Column(String)
    update_date = Column(String, nullable=False)
    language = Column(String)
    subtitles = Column(String)
    release_date = Column(String)
    download_size = Column(String)
    director = Column(String)
    duration = Column(String)
    country = Column(String)

    genres = relationship("MovieGenre", secondary="movie_to_genre",
                          lazy="selectin")

    actors = relationship("MovieActor", secondary="movie_to_actor",
                          lazy="selectin")

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", lazy="selectin", viewonly=True)
