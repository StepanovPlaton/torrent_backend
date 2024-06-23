from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import relationship

from ..database import Base


class GameGenre(Base):
    __tablename__ = "game_genres"

    id = Column(Integer, primary_key=True)
    genre = Column(String, nullable=False, unique=True)

    games = relationship("Game", secondary="game_to_genre",
                         lazy="selectin")


class GameToGenre(Base):
    __tablename__ = "game_to_genre"
    __table_args__ = (
        PrimaryKeyConstraint("game_id", "genre_id"),
    )

    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    genre_id = Column(Integer, ForeignKey("game_genres.id"), nullable=False)
