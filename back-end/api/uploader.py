from typing import List

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from dotenv import load_dotenv
from .s3 import *


router = APIRouter()

load_dotenv(dotenv_path = ".env")

access_key_id = os.getenv('access_key_ID')
access_key_pass = os.getenv('access_key_PASS')
s3 = s3_connection (access_key_id, access_key_pass)

@router.post("/uploadfiles")
def create_upload_files(
    father_image: UploadFile = File(...),
    mother_image: UploadFile = File(...),
    ):
    father = s3_put_object(s3, "12war", father_image.filename, "man/test_image.jpg") 
    mother = s3_put_object(s3, "12war", mother_image.filename, "woman/test_image.jpg") 
    tmp_url = s3_get_image_url(s3,'man/test_image')
    return {"tmp_url":tmp_url}

@router.get("/")
def uploader():
    content = """
<body>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="father_image" type="file">
<input name="mother_image" type="file">
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


