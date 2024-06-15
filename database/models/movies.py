from sqlalchemy import Column, ForeignKey, Integer, String

from ..database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)

    title = Column(String, nullable=False, unique=True)
    cover = Column(String)
    age = Column(String)
    description = Column(String)

    torrent_file = Column(String, nullable=False)
    upload_date = Column(String, nullable=False)
    trailer = Column(String)
    update_date = Column(String, nullable=False)
    language = Column(String)
    subtitles = Column(String)
    release_date = Column(String)
    download_size = Column(String)
    director = Column(String)
    duration = Column(String)
    country = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))
