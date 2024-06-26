from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Audiobook(Base):
    __tablename__ = "audiobooks"

    id = Column(Integer, primary_key=True)

    title = Column(String, nullable=False, unique=True)
    cover = Column(String)
    description = Column(String)
    author = Column(String)

    torrent_file = Column(String, nullable=False)
    fragment = Column(String)
    update_date = Column(String, nullable=False)
    language = Column(String)
    release_date = Column(String)
    download_size = Column(String)
    duration = Column(String)
    reader = Column(String)

    genres = relationship("AudiobookGenre", secondary="audiobook_to_genre",
                          lazy="selectin")

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", lazy="selectin", viewonly=True)
