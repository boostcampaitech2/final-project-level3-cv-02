from typing import List

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse

router = APIRouter()


@router.post("/uploadfiles")
def create_upload_files(files: List[UploadFile] = File(...)):
    print({"filenames": [file.filename for file in files]})
    return FileResponse("mlops.png")


@router.get("/")
def uploader():
    content = """
<body>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file">
<input name="files" type="file">
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


