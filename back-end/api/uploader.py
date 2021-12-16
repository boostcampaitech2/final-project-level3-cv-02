import io
from PIL import Image
from typing import List
import uuid
import shutil
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from dotenv import load_dotenv
from .s3 import *

import sys
import os
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"../")))
from babygan import *

router = APIRouter()

load_dotenv(dotenv_path = ".env")

access_key_id = os.getenv('access_key_ID')
access_key_pass = os.getenv('access_key_PASS')
s3 = s3_connection (access_key_id, access_key_pass)

def inference_t (mother, father, u2id):
    mother_image_url = s3_get_image_url(s3, "woman/"+mother)
    father_image_url = s3_get_image_url(s3,"man/"+father)
    baby_path = inference_test.do_inference(mother_image_url, father_image_url, u2id[:8])
    
    s3_put_object(s3, "12war",baby_path, f"baby/{u2id}Baby.png" )
    #shutil.rmtree(baby_path[:-12])   # /final9.png

@router.post("/uploadfiles")
def create_upload_files(
    father_image: UploadFile = File(...),
    mother_image: UploadFile = File(...),
    ):
    setting_uuid = str(uuid.uuid4())
    father_image_name=setting_uuid+"Father.png"#father_image.filename
    mother_image_name=setting_uuid+"Mother.png"#mother_image.filename
    s3.upload_fileobj(
        father_image.file, "12war", "man/"+father_image_name, ExtraArgs={"ContentType": "image/png", "ACL": "public-read"}
    )
    s3.upload_fileobj(
        mother_image.file, "12war", "woman/"+mother_image_name, ExtraArgs={"ContentType": "image/png", "ACL": "public-read"}
    )
    inference_t(mother_image_name, father_image_name, setting_uuid)
    baby_image_path = s3_get_image_url(s3,'baby/'+setting_uuid+"Baby.png") 
    return { "baby_image_path": baby_image_path }

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


