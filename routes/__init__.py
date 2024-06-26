from .games import games_router as games_router
from .game_genres import game_genres_router as game_genres_router

from .movies import movies_router as movies_router
from .movie_actors import movie_actors_router as movie_actors_router
from .movie_genres import movie_genres_router as movie_genres_router

from .audiobooks import audiobooks_router as audiobooks_router
from .audiobook_genres import audiobook_genres_router as audiobook_genres_router

from .files import files_router as files_router
from .startup import startup_router as startup_router
from .auth import auth_router as auth_router
