from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    hash_of_password = Column(String, nullable=False)

    games = relationship("Game", viewonly=True)
    movies = relationship("Movie", viewonly=True)
    audiobooks = relationship("Audiobook", viewonly=True)
