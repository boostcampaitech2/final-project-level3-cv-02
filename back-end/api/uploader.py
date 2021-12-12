from typing import List

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from dotenv import load_dotenv
from .s3 import *

router = APIRouter()

#s3 = s3_connection()
load_dotenv(dotenv_path = ".env")

access_key_id = os.getenv('access_key_ID')
access_key_pass = os.getenv('access_key_PASS')
s3 = s3_connection (access_key_id, access_key_pass)

@router.post("/uploadfiles")
def create_upload_files(files: List[UploadFile] = File(...)):
    print({"filenames": [file.filename for file in files]})
    temp = s3_put_object(s3,"12war", files[0].filename, "man/test_image.jpg") 
    temp2 = s3_put_object(s3,"12war", files[1].filename, "woman/test_image.jpg") 
    print(temp)
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


