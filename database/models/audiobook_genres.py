from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import relationship

from ..database import Base


class AudiobookGenre(Base):
    __tablename__ = "audiobook_genres"

    id = Column(Integer, primary_key=True)
    genre = Column(String, nullable=False, unique=True)

    audiobooks = relationship("Audiobook", secondary="audiobook_to_genre",
                              lazy="selectin")


class AudiobookToGenre(Base):
    __tablename__ = "audiobook_to_genre"
    __table_args__ = (
        PrimaryKeyConstraint("audiobook_id", "genre_id"),
    )

    audiobook_id = Column(Integer, ForeignKey("audiobooks.id"), nullable=False)
    genre_id = Column(Integer, ForeignKey(
        "audiobook_genres.id"), nullable=False)
