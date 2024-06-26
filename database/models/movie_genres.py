from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import relationship

from ..database import Base


class MovieGenre(Base):
    __tablename__ = "movie_genres"

    id = Column(Integer, primary_key=True)
    genre = Column(String, nullable=False, unique=True)

    movies = relationship("Movie", secondary="movie_to_genre",
                          lazy="selectin", viewonly=True)


class MovieToGenre(Base):
    __tablename__ = "movie_to_genre"
    __table_args__ = (
        PrimaryKeyConstraint("movie_id", "genre_id"),
    )

    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    genre_id = Column(Integer, ForeignKey("movie_genres.id"), nullable=False)
