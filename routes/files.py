from fastapi import APIRouter, HTTPException, UploadFile

from database import *
from file_handler import *

files_router = APIRouter(prefix="/files", tags=["Files"])


@files_router.post("/torrent", response_model=str)
async def upload_torrent(torrent: UploadFile):
    try:
        return await save_torrent_file(torrent)
    except Exception as ex:
        print(ex)
        raise HTTPException(500, detail=str(ex))


@files_router.post("/cover", response_model=str)
async def upload_cover(cover: UploadFile):
    try:
        return await save_image(cover, "cover")
    except Exception as ex:
        print(ex)
        raise HTTPException(500, detail=str(ex))


@files_router.post("/audio", response_model=str)
async def upload_audio_fragment(fragment: UploadFile):
    try:
        return await save_audio_fragment(fragment)
    except Exception as ex:
        print(ex)
        raise HTTPException(500, detail=str(ex))
