from sqlalchemy.orm import Session
from ..model import models, schemas

def get_user_statistic(db: Session):
    return db.query(UserStatistic).all()