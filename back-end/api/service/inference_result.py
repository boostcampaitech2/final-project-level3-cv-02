import sys 
import os
from sqlalchemy.orm import Session
from sqlalchemy import update
from sqlalchemy.sql import func

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append("../")
from ..model import models, schemas

def create_inference_result(db: Session, inference_result: schemas.InferenceResultCreate):
    """
    사용자가 아기얼굴생성하기 버튼을 누르면 입력한 정보를 DB 내 inference_result 테이블에 저장합니다. 

    Args: 
        db: 업데이트할 db session
        inference_result: 사용자가 입력한 테이블 구조에 맞는 데이터 집합
    Return:
        db_result: 생성된 inference_result 테이블내의 tuple 
    """
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
    
def get_inference_results(db: Session):
    """
    InferenceResult 테이블의 내용을 반환합니다.
    """
    return db.query(models.InferenceResult).all()

def update_comment(db: Session, uuid: str, comment: str):
    """
    사용자가 입력한 comment를 db에 저장합니다.

    Args:
        db: 업데이트할 db session
        uuid: 사용자의 uuid
        comment: 사용자가 작성한 comment
    Return:
        db_share: comment가 업데이트 된 db session(?) 
    """
    db_share = db.query(models.InferenceResult).filter(models.InferenceResult.id==uuid).one()
    db_share.comment = comment
    db.commit()
    return db_share

def update_inference_fail (db:Session, uuid: str):
    """
    inference 중 이탈한 사용자의 이탈시점을 db에 저장합니다.

    Args:
        db: 업데이트할 db session
        uuid: 사용자의 uuid
    Return:
        db_update: 이탈시점이 저장된 db
    """
    db_update = db.query(models.InferenceResult).filter(models.InferenceResult.id == uuid).one()
    if not db_update.complete:
        db_update.closed_at = func.now()
        db.commit()
    return db_update

def update_inference_result (db:Session, uuid: str, baby_url:str ):
    """
    inference가 끝나고 사용자가 이탈하지 않은 상태라면 결과물과 종료시점을 db에 저장합니다.

    Args: 
        db: 업데이트할 db session
        uuid: 사용자의 uuid
        baby_url: S3의 생성된 이미지 url
    Return:
        db_update: 종료시점과 baby_url이 저장된 db
    """
    db_update = db.query(models.InferenceResult).filter(models.InferenceResult.id == uuid).one()
    if db_update.complete: 
        db_update.closed_at = func.now() 
        db_update.baby_url = baby_url 
        db.commit()
    return db_update

def update_stop_inference(db:Session, uuid: str):
    """
    inference 중 이탈한 사용자 tuple을 반환합니다.
    Args:
        db: 업데이트할 db session
        uuid: 사용자의 uuid
    Return:
        db_false: 이탈한 사용자 tuple 
    """
    db_false = db.query(models.InferenceResult).filter(models.InferenceResult.id == uuid).one()
    return db_false

