
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    cover = Column(String)
    title = Column(String, nullable=False, unique=True)
    description = Column(String)
    torrent_file = Column(String, nullable=False)
    language = Column(String)
    version = Column(String)
    download_size = Column(String)
    upload_date = Column(String)

    system = Column(String)
    processor = Column(String)
    memory = Column(String)
    graphics = Column(String)
    storage = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="games")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    hash_of_password = Column(String, nullable=False)

    games = relationship("Game", back_populates="owner")
