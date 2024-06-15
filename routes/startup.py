from fastapi import APIRouter
from pathlib import Path

from env import Env

startup_router = APIRouter()


def create_folders():
    need_paths = [
        Path() / "content" / "images" / "cover" / "full_size",
        Path() / "content" / "images" / "cover" / "preview",
        Path() / "content" / "images" / "screenshot" / "full_size",
        Path() / "content" / "images" / "screenshot" / "preview",
        Path() / "content" / "torrent",
        Path() / "content" / "audio"
    ]
    for path in need_paths:
        path.mkdir(parents=True, exist_ok=True)


@startup_router.on_event("startup")
def startup():
    create_folders()
