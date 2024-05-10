from fastapi import APIRouter
from pathlib import Path

router = APIRouter()

@router.on_event("startup")
def startup():
    need_paths = [
        Path() / "content" / "images" / "cover" / "full_size",
        Path() / "content" / "images" / "cover" / "preview",
        Path() / "content" / "images" / "screenshot" / "full_size",
        Path() / "content" / "images" / "screenshot" / "preview",
        Path() / "content" / "torrent"
    ]
    for path in need_paths:
        path.mkdir(parents=True, exist_ok=True)