import io
from PIL import Image
from typing import List, Optional
import uuid
import shutil
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from dotenv import load_dotenv
import shutil
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append("../")

from .s3 import *
from ..config.s3 import s3_connection

load_dotenv(dotenv_path=".env")
access_key_id = os.getenv("access_key_ID")
access_key_pass = os.getenv("access_key_PASS")
s3 = s3_connection(access_key_id, access_key_pass)


def upload_image(common_uuid: str, image: File(...), file_name: str):
    """
    image의 url을 추출하고 DB에 저장합니다.
    Args:
        common_uuid : father, mother, baby의 공통 uuid
        image : image file
        file_name : Father, Mother, Baby
    Return:
        generated image url
    """
    image_name = common_uuid + file_name + ".png"
    save_path = file_name + "/" + image_name
    if file_name == "baby":
        s3_put_object(
            s3,
            "12war",
            image,
            save_path,
        )
    else:
        s3.upload_fileobj(
            image.file,
            "12war",
            save_path,
            ExtraArgs={"ContentType": "image/png", "ACL": "public-read"},
        )
    image_url = s3_get_image_url(s3, save_path)
    return image_url
