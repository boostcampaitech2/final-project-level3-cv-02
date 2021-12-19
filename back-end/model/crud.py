from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import Depends

def get_inference_results(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.InferenceResult).offset(skip).limit(limit).all()

def create_inference_result(db: Session, inference_result: schemas.InferenceResultCreate):
    db_result = models.InferenceResult(
        id = inference_result['id'],
        father_url = inference_result['father_url'],
        mother_url = inference_result['mother_url'],
        baby_url = inference_result['baby_url'],
        comment = inference_result['comment']
    )
    print(db)
    print(db_result)
    # print(list(db))
    print("db_result")
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result
