from sqlalchemy.orm import Session
from . import models, schemas

def get_inference_results(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.InferenceResult).offset(skip).limit(limit).all()

# def create_inference_result(db: Session, inference_result: schemas.InferenceResultCreate):

#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
