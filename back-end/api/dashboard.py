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


@router.get("/dashboard")
def get_user_info():
    """
    성별과 나이에 따른 유입량을 반환합니다.
    Return:
        list : 남성, 여성, 전체 이용자의 나이대 별 유입 횟수
    """
    entrance_by_gender = [
        {"gender": "Male", "count": [1, 1, 1, 1, 1]},
        {"gender": "Female", "count": [2, 2, 2, 2, 2]},
        {"gender": "Total", "count": [3, 3, 3, 3, 3]}
    ]

    return entrance_by_gender


