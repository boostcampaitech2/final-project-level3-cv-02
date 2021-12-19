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
        return db
    finally:
        db.close()


@router.get("/dashboard/inflow")
def get_user_inflow():
    """
    성별과 나이에 따른 유입량을 반환합니다.
    Return:
        list : 남성, 여성, 전체 이용자의 나이대 별 유입 횟수
    """
    inflow_by_gender = [
        {"gender": "Male", "count": [1, 1, 1, 1, 1]},
        {"gender": "Female", "count": [2, 2, 2, 2, 2]},
        {"gender": "Total", "count": [3, 3, 3, 3, 3]}
    ]

    return inflow_by_gender

@router.get("/dashboard/bounce_rate")
def get_bounce_rate():
    """
    결과물이 나올 때까지 기다린 사람과 이탈한 사람의 수를 반환합니다.
    Return:
        list : 기다린 사람과 이탈한 사람의 수
    """
    stay = 0
    no_stay = 0

    db = get_db()

    users = crud.get_inference_results(db, skip=0, limit=100)

    for user in users:
        print(user)
        if user.complete:
            stay += 1
        else:
            no_stay += 1

    bounce_rate = [{"stay":stay, "no_stay":no_stay}] 

    return bounce_rate
