import io
from PIL import Image
from typing import List, Optional
import uuid
import shutil
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from dotenv import load_dotenv
from .s3 import *
import shutil 


# router = APIRouter()

load_dotenv(dotenv_path = ".env")
access_key_id = os.getenv('access_key_ID')
access_key_pass = os.getenv('access_key_PASS')
s3 = s3_connection (access_key_id, access_key_pass)

def upload_image(
    common_uuid : str,
    image1: File(...),
    image2: Optional[str] = None
    ):
    """
    image의 url을 추출하고 DB에 저장합니다.
    image가 2개 들어오는 경우(부모 이미지 저장)와 1개 들어오는 경우(자식)를 커버합니다.
    Args:
        common_uuid : father, mother, baby의 공통 uuid
        image1 : Father image if image2 exist else Baby image
        image2 : Mother image if exist else None
    Return:
        generated image url
    """
    if image2:
        father_image_name = common_uuid + "Father.png"
        mother_image_name = common_uuid + "Mother.png"

        s3.upload_fileobj(
            image1.file, "12war", "man/"+father_image_name, 
            ExtraArgs={"ContentType": "image/png", "ACL": "public-read"}
        )
        s3.upload_fileobj(
            image2.file, "12war", "woman/"+mother_image_name, 
            ExtraArgs={"ContentType": "image/png", "ACL": "public-read"}
        )
        
        father_url = s3_get_image_url(s3, "man/"+father_image_name)
        mother_url = s3_get_image_url(s3, "woman/"+mother_image_name)
        
        return father_url, mother_url
    
    else:
        baby_image_name = common_uuid + "Baby.png"
        
        s3.upload_fileobj(
            image1.file, "12war", "baby/"+baby_image_name, 
            ExtraArgs={"ContentType": "image/png", "ACL": "public-read"}
        )

        baby_url = s3_get_image_url(s3, "baby/"+baby_image_name)

        return baby_url


