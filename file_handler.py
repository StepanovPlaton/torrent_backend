import hashlib
from io import BytesIO
import mimetypes
from pathlib import Path
from typing import Literal
import aiofiles
from fastapi import UploadFile
from PIL import Image

def create_hash_name(filename: str):
    return str(hashlib.sha1(filename.encode()).hexdigest())

async def save_torrent_file(torrent: UploadFile):
    hash_filename = create_hash_name(torrent.filename)+".torrent"
    async with aiofiles.open(Path() / "content" / "torrent" 
                            / hash_filename, 'wb') as file:
        await file.write(await torrent.read())
        return hash_filename

async def save_image(cover: UploadFile, type: Literal["cover", "screenshot"]):
    hash_filename = create_hash_name(cover.filename) \
                        + mimetypes.guess_extension(cover.content_type)
    async with aiofiles.open(Path() / "content" / "images" / type / "full_size"  
                            / hash_filename, 'wb') as full_size_file, \
                aiofiles.open(Path() / "content" / "images" / type / 
                                 "preview" / hash_filename, 'wb') as preview_file:
        cover_data = await cover.read()
        await full_size_file.write(cover_data)
        image = Image.open(BytesIO(cover_data))
        compressed_coefficient = (image.size[0] * image.size[1]) / (1280*720/4)
        if(compressed_coefficient < 1): compressed_coefficient = 1
        compressed_image = image.resize(
            (   int(image.size[0] / compressed_coefficient),
                int(image.size[1] / compressed_coefficient)   )
        )

        buf = BytesIO()
        compressed_image.save(buf, format=
                   cover.content_type.upper().replace("IMAGE/", ""))    
        await preview_file.write(buf.getbuffer())
        return hash_filename    
    