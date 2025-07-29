from pathlib import Path
from fastapi import File, HTTPException, UploadFile, APIRouter
from fastapi.responses import FileResponse
import shutil

router = APIRouter(
    prefix='/files',
    tags=['Files']
)

@router.post('/upload/')
def upload_file(file:UploadFile=File(...)):
    file_path = f"uploaded/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename}



@router.get('/download/{file_path}')
async def download_file(file_path: str):
    upload_dir = Path("uploaded")
    file_location = upload_dir / file_path

    try:
        # Prevent path traversal (e.g., '../../etc/passwd')
        file_location = file_location.resolve()
        if not file_location.is_file() or not file_location.is_relative_to(upload_dir.resolve()):
            raise HTTPException(status_code=404, detail="File not found")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid file path")

    return FileResponse(
        path=file_location,
        media_type='application/octet-stream',
        filename=file_location.name
    )



