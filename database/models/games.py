from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    cover = Column(String)
    description = Column(String)
    torrent_file = Column(String, nullable=False)
    upload_date = Column(String, nullable=False)
    trailer = Column(String)

    system = Column(String)
    processor = Column(String)
    memory = Column(String)
    graphics = Column(String)
    storage = Column(String)

    version = Column(String)
    update_date = Column(String, nullable=False)
    developer = Column(String)
    language = Column(String)
    release_date = Column(String)
    download_size = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))
