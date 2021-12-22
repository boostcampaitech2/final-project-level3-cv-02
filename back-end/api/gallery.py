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
from babygan import inference

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
        return db
    finally:
        db.close()

@router.get("/gallery")
def get_image_url():
    """
    gallery에 표시될 이미지 url을 반환합니다.
    Return:
        list : father_url, mother_url, baby_url을 담은 list 반환
    """
    urls = []

    db = get_db()

    users = crud.get_inference_results(db)

    for i, user in enumerate(users):
        if user.comment:
            urls.append({"father_url": user.father_url, "mother_url": user.mother_url, "baby_url": user.baby_url, "comment": user.comment})
    
    return urls


# class ShareParam(BaseModel):
#     uuid: str
#     comment: str
    
@router.post("/share")
def share_image(body:dict):
    uuid = body['uuid']
    comment = body['comment']
    print(uuid)
    print(comment)
    db = get_db()
    crud.update_comment(db, uuid, comment)

    


