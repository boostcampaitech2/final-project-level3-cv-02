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
    inflow_by_gender = [{
        "Male": [1, 1, 1, 1, 1],
        "Female": [2, 2, 2, 2, 2],
        "Total": [3, 3, 3, 3, 3]
    }]

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


@router.get("/dashboard/time")
def get_time():
    """
    이탈한 평균 시간과 inference 평균 시간을 반환합니다.
    Return:
        list : 이탈한 평균 시간(bound_time)과 inference 평균 시간의 리스트
    """
    db = get_db()

    users = crud.get_inference_results(db, skip=0, limit=100)

    bounce_time = None
    inference_time = None

    bounce_cnt = 0
    inference_cnt = 0

    for user in users:
        tmp_time = user.closed_at - user.created_time
        if not user.complete:
            try:
                if bounce_time:
                    bounce_time += tmp_time 
                else :
                    bounce_time = tmp_time 
                bounce_cnt += 1
            except:
                print("TypeError: DateTime is NoneType")
        else:
            try:
                if inference_time:
                    inference_time += tmp_time
                else:
                    inference_time = tmp_time
                inference_time += 1

    
    average_bounce_time = bounce_time / bounce_cnt
    average_inference_time = inference_time / inference_cnt

    return [{"bounce_time": average_bounce_time, "inference_time": average_inference_time}]
    

