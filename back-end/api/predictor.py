import io
from PIL import Image
from typing import List
import uuid
import shutil
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from dotenv import load_dotenv
from .s3 import *
from .uploader import upload_image
import shutil 
from babygan import inference_test


router = APIRouter()
load_dotenv(dotenv_path = ".env")

@router.post("/uploadfiles") # 추후에 uploadfiles 이름 변경 -> predict
def predict(
    father_image: UploadFile = File(...),
    mother_image: UploadFile = File(...),
    ):
    """
    inference를 위한 함수입니다.
    Args:
        father_image : 사용자가 upload한 Father image file
        mother_image : 사용자가 upload한 Mother image file
    Return:
        baby_url : S3에서 추출한 결과물 url을 반환합니다.
    """
    # TODO: 부모 이미지 S3에 저장 -> uploader
    setting_uuid = str(uuid.uuid4())
    father_url, mother_url = upload_image(setting_uuid, father_image, mother_image)
    
    # TODO: 찐 인퍼런스
    ## 이 부분 저장하지 않고 바꾸는 걸로 수정해야 함
    ## 기존 코드에서 엄마 아빠 순으로 넣고 있어서 수정
    baby_file_path = inference_test.do_inference(father_url, mother_url, setting_uuid[:8])

    # TODO: 벱비 이미지 S3에 저장
    ## baby_file_path 제대로 전달되는지 확인 필요(file이 맞는지)
    baby_url = upload_image(setting_uuid, baby_file_path)

    # TODO: 벱비 url return
    return { "baby_image_path": baby_url }

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


