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


@router.get("/dashboard/inflow")
def get_user_inflow():
    """
    성별과 나이에 따른 유입량을 반환합니다.
    Return:
        list : 남성, 여성, 전체 이용자의 나이대 별 유입 횟수
    """
    inflow_by_gender = {
        "Male": [1, 1, 1, 1, 1],
        "Female": [2, 2, 2, 2, 2],
        "Total": [3, 3, 3, 3, 3]
    }

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

    users = crud.get_inference_results(db)

    for user in users:
        if user.complete:
            stay += 1
        else:
            no_stay += 1

    bounce_rate = {"stay":stay, "no_stay":no_stay}

    return bounce_rate


@router.get("/dashboard/time")
def get_time():
    """
    이탈한 평균 시간과 inference 평균 시간을 반환합니다.
    Return:
        list : 이탈한 평균 시간(bound_time)과 inference 평균 시간의 리스트
    """
    db = get_db()

    statistic = crud.get_statistic(db)

    bounce_time = statistic.avg_bounce_time
    inference_time = statistic.avg_inference_time

    return {"bounce_time": bounce_time, "inference_time": inference_time}
    

@router.get("/dashboard/attempts")
def get_num_of_attempts():
    """
    총 시도 횟수를 반환합니다.
    Return:
        json : 총 시도 횟수
    """
    db = get_db()

    users = crud.get_inference_results(db)

    return {"attempts": len(users)}

