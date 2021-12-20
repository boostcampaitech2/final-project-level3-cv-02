from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import Depends
from sqlalchemy import update
from sqlalchemy.sql import func

# stmt = (
#     update(user_table).
#     where(user_table.c.id == 5).
#     values(name='user #5')
# )

def get_inference_results(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.InferenceResult).offset(skip).limit(limit).all()

def create_inference_result(db: Session, inference_result: schemas.InferenceResultCreate):
    db_result = models.InferenceResult(
        id = inference_result['id'],
        father_url = inference_result['father_url'],
        mother_url = inference_result['mother_url'],
        baby_url = inference_result['baby_url'],
        comment = inference_result['comment'],
        complete = inference_result['complete'] # True
    )
    db.add(db_result)
    db.commit()
    return db_result

def update_inference_result (db:Session, uuid: str, baby_url:str ):#, comment:str)  # inference_result:schemas.InferenceResultCreate):
    
    db_update = db.query(models.InferenceResult).filter(models.InferenceResult.id == uuid).one()

    print (db_update)

    if not db_update.complete: #실패 
        db_update.closed_at = func.now() # baby_url =  None 
        db_update.baby_url = None 
    else:  #성공 
        db_update.closed_at = func.now()
        db_update.baby_url = baby_url 

    db.commit()

    return db_update

