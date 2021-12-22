import sys
import os
from sqlalchemy.orm import Session
from sqlalchemy import update
from sqlalchemy.sql import func

sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
)
sys.path.append("../")
from ..model import models, schemas


def create_inference_result(
    db: Session, inference_result: schemas.InferenceResultCreate
):
    db_result = models.InferenceResult(
        id=inference_result["id"],
        father_url=inference_result["father_url"],
        mother_url=inference_result["mother_url"],
        baby_url=inference_result["baby_url"],
        comment=inference_result["comment"],
        complete=inference_result["complete"],  # True
        gender=inference_result["gender"],
        age=inference_result["age"],
    )
    db.add(db_result)
    db.commit()
    return db_result


def get_inference_results(db: Session):
    return db.query(models.InferenceResult).all()


def update_comment(db: Session, uuid: str, comment: str):
    db_share = (
        db.query(models.InferenceResult)
        .filter(models.InferenceResult.id == uuid)
        .one()
    )
    db_share.comment = comment
    db.commit()
    return db_share


def update_inference_fail(db: Session, uuid: str):
    db_update = (
        db.query(models.InferenceResult)
        .filter(models.InferenceResult.id == uuid)
        .one()
    )
    if not db_update.complete:
        db_update.closed_at = func.now()
        db.commit()
    return db_update


def update_inference_result(
    db: Session, uuid: str, baby_url: str
):
    db_update = (
        db.query(models.InferenceResult)
        .filter(models.InferenceResult.id == uuid)
        .one()
    )
    if db_update.complete:
        db_update.closed_at = func.now()
        db_update.baby_url = baby_url
        db.commit()
    return db_update


def update_stop_inference(db: Session, uuid: str):
    db_false = (
        db.query(models.InferenceResult)
        .filter(models.InferenceResult.id == uuid)
        .one()
    )
    return db_false
