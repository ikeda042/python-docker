from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from .crud import STORAGE_DIR, iter_file, list_files, save_upload_file

router = APIRouter(prefix="/files", tags=["files"])


@router.get("/")
async def get_files() -> list[str]:
    """List all stored filenames."""
    return await list_files()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)) -> dict[str, str]:
    """Upload a new file to storage."""
    filename = await save_upload_file(file)
    return {"filename": filename}


@router.get("/{filename}")
async def download_file(filename: str) -> StreamingResponse:
    """Download a file from storage."""
    file_path = STORAGE_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return StreamingResponse(iter_file(file_path), headers=headers)
