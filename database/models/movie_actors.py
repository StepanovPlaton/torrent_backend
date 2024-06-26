from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import relationship

from ..database import Base


class MovieActor(Base):
    __tablename__ = "movie_actors"

    id = Column(Integer, primary_key=True)
    actor = Column(String, nullable=False, unique=True)

    movies = relationship("Movie", secondary="movie_to_actor",
                          lazy="selectin", viewonly=True)


class MovieToActor(Base):
    __tablename__ = "movie_to_actor"
    __table_args__ = (
        PrimaryKeyConstraint("movie_id", "actor_id"),
    )

    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    actor_id = Column(Integer, ForeignKey("movie_actors.id"), nullable=False)
