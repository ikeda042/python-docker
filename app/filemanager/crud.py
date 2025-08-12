from __future__ import annotations

from pathlib import Path
from typing import AsyncIterator, List

import anyio
from fastapi import UploadFile

# Directory where files will be stored
STORAGE_DIR = Path(__file__).resolve().parent / "storage"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)


async def save_upload_file(upload_file: UploadFile) -> str:
    """Persist an uploaded file asynchronously."""
    destination = STORAGE_DIR / upload_file.filename
    async with await anyio.open_file(destination, "wb") as out_file:
        while True:
            chunk = await upload_file.read(1024 * 1024)
            if not chunk:
                break
            await out_file.write(chunk)
    await upload_file.close()
    return upload_file.filename


async def list_files() -> List[str]:
    """Return a list of stored filenames."""
    return await anyio.to_thread.run_sync(
        lambda: [p.name for p in STORAGE_DIR.iterdir() if p.is_file()]
    )


async def iter_file(path: Path, chunk_size: int = 1024 * 1024) -> AsyncIterator[bytes]:
    """Yield file chunks asynchronously."""
    async with await anyio.open_file(path, "rb") as file:
        while True:
            chunk = await file.read(chunk_size)
            if not chunk:
                break
            yield chunk
