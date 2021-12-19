import io
from PIL import Image
from typing import List
import uuid
import shutil
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from dotenv import load_dotenv
from .s3 import *
from .uploader import upload_image
import shutil 
from babygan import inference_test

from sqlalchemy.orm import Session

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append("../")

from model import crud, models, schemas
from model.database import SessionLocal, engine


router = APIRouter()
load_dotenv(dotenv_path = ".env")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @router.get("/users/", response_model=List[schemas.InferenceResult])
def read_queries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_inference_results(db, skip=skip, limit=limit)

# @router.post("/users",response_model=schemas.InferenceResult)
def create_query(inference_result:schemas.InferenceResultCreate, db: Session = Depends(get_db)):
    return crud.create_inference_result(db, inference_result=inference_result.dict())

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
    setting_uuid = str(uuid.uuid4())
    father_url = upload_image(setting_uuid, father_image, "father")
    mother_url = upload_image(setting_uuid, mother_image, "mother")
    
    # baby_file_path = inference_test.do_inference(father_url, mother_url, setting_uuid[:8])

    # baby_url = upload_image(setting_uuid, baby_file_path, "baby")

    create_query(inference_result = ({"id":setting_uuid, "father_url":father_url, "mother_url":mother_url, "baby_url":"baby_url_test"}))

    return { "baby_image_path": "baby_url" } # 요거 주석처리 한 것

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


