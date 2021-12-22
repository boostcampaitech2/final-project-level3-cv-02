import os
import sys
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append("../")
from ..model import models, schemas


def get_statistic(db: Session):
    return db.query(models.Statistic).one()
