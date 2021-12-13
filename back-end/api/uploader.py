import io
from PIL import Image
from typing import List
import uuid

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from dotenv import load_dotenv
from .s3 import *
import sys
import os
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'../../../'))) # 상위에 상위라서
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
import babygan

router = APIRouter()

load_dotenv(dotenv_path = ".env")
#ln -s /usr/local/cuda-11.0/targets/x86_64-linux/lib/libcusolver.so.10 /usr/local/cuda-11.0/targets/x86_64-linux/lib/libcusolver.so.11

access_key_id = os.getenv('access_key_ID')
access_key_pass = os.getenv('access_key_PASS')
s3 = s3_connection (access_key_id, access_key_pass)
#https://12war.s3.ap-northeast-2.amazonaws.com/man/e6fb043b-5dd4-42e1-a0a2-b3651787170c%E1%84%8E%E1%85%A1%E1%84%8B%E1%85%B3%E1%86%AB%E1%84%8B%E1%85%AE.jpeg
def inference(father_image_name, mother_image_name): #여기서 babygan.inferenc
    father_image = s3_get_image_url(s3,father_image_name)
    mother_image = s3_get_image_url(s3,father_image_name) #이거두개를 
    temp_cha = "https://12war.s3.ap-northeast-2.amazonaws.com/man/e6fb043b-5dd4-42e1-a0a2-b3651787170c%E1%84%8E%E1%85%A1%E1%84%8B%E1%85%B3%E1%86%AB%E1%84%8B%E1%85%AE.jpeg"
    temp_jung = "https://12war.s3.ap-northeast-2.amazonaws.com/woman/9d01189d-5214-4251-ae09-169e8ceb348c%E1%84%8C%E1%85%A5%E1%86%BC%E1%84%8E%E1%85%A2%E1%84%8B%E1%85%A7%E1%86%AB.jpeg"
    babygan.inference_test.main(temp_cha,temp_jung)  
    

@router.post("/uploadfiles")
def create_upload_files(
    father_image: UploadFile = File(...),
    mother_image: UploadFile = File(...),
    ):
    setting_uuid = str(uuid.uuid4())
    father_image_name=setting_uuid+father_image.filename
    mother_image_name=setting_uuid+mother_image.filename
    s3.upload_fileobj(
        father_image.file, "12war", "man/"+father_image_name, ExtraArgs={"ContentType": "image/png", "ACL": "public-read"}
    )
    s3.upload_fileobj(
        mother_image.file, "12war", "woman/"+mother_image_name, ExtraArgs={"ContentType": "image/png", "ACL": "public-read"}
    )#
    
    inference(father_image_name, mother_image_name) #여기서 애엄마 애아빠 사진 보냄
    # 추후 아기사진 올리고 받아와야함
    # 아기 사진도 같은 uuid쓰면됨(setting_uuid)
    baby_image_path = s3_get_image_url(s3,'baby/field-6558125_1920')
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


