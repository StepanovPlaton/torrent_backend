from fastapi import APIRouter, Depends, HTTPException, UploadFile

from database import *
from file_handler import *

router = APIRouter(prefix="/files", tags=["Files"])

@router.post("/torrent", response_model=str)
async def upload_torrent(torrent: UploadFile):
    try: return await save_torrent_file(torrent)
    except Exception as ex: 
        print(ex)
        raise HTTPException(500)

@router.post("/cover", response_model=str)
async def upload_cover(cover: UploadFile):
    try: return await save_image(cover, "cover")
    except Exception as ex: 
        print(ex)
        raise HTTPException(500)
