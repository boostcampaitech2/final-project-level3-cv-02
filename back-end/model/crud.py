from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import Depends
from sqlalchemy import update
from sqlalchemy.sql import func

def get_inference_results(db: Session):
    return db.query(models.InferenceResult).all()


def get_user_statistic(db: Session):
    return db.query(models.UserStatistic).all()

def get_statistic(db: Session):
    return db.query(models.Statistic).one()

def create_inference_result(db: Session, inference_result: schemas.InferenceResultCreate):
    db_result = models.InferenceResult(
        id = inference_result['id'],
        father_url = inference_result['father_url'],
        mother_url = inference_result['mother_url'],
        baby_url = inference_result['baby_url'],
        comment = inference_result['comment'],
        complete = inference_result['complete'], # True
        gender = inference_result['gender'],
        age = inference_result['age']
    )
    db.add(db_result)
    db.commit()
    return db_result

def update_inference_result (db:Session, uuid: str, baby_url:str ):
    
    db_update = db.query(models.InferenceResult).filter(models.InferenceResult.id == uuid).one()

    if not db_update.complete: #실패 
        db_update.closed_at = func.now() # baby_url =  None 
        db_update.baby_url = None 
    else:  # 성공 
        db_update.closed_at = func.now()
        db_update.baby_url = baby_url 

    db.commit()

    return db_update

def update_comment(db: Session, uuid: str, comment: str):
    db_share = db.query(models.InferenceResult).filter(models.InferenceResult.id==uuid).one()

    db_share.comment = comment

    db.commit()

    return db_share
