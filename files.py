from typing import Annotated

from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/files")
async def create_file(files: Annotated[list[bytes] | None, File()] = None):
    if not files:
        return {"message": "No file sent"}
    else:
        return {"file_size": [len(file) for file in files]}


@app.post("/uploadfiles")
async def create_upload_file(files: Annotated[list[UploadFile] | None, File(description="Multiple files")] =None):
    if not files:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="You must upload a file")
    else:
        return {"filename": [files.filename for file in files]}