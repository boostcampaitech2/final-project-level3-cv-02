import sys 
import os
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from api.config.database import Base

class Statistic(Base):
    """
    airflow batchjob 결과물을 저장하는 table 입니다
    Columns: 
        avg_bounce_time, total_user, avg_inference_time
    """
    __table_args__ = {'extend_existing': True}
    __tablename__ = "statistic"
    avg_bounce_time = Column(Integer, primary_key=True)
    total_user = Column(Integer)
    avg_inference_time = Column(Integer)

class UserStatistic(Base):
    """
    대시보드를 위한 사용자 정보를 저장하는 table 입니다.
    Columns: 
        id, gender, age, rate
    """
    __table_args__ = {'extend_existing': True}
    __tablename__ = "user_statistic"
    id = Column(Integer, primary_key=True)
    gender = Column(String)
    age = Column(Integer)
    rate = Column(Float)
    

class InferenceResult(Base):
    """
    사용자가 입력한 정보(이미지 url, 성별 등)와 결과물 url을 저장하는 table 입니다.
    Columns:
        id, father_image_url, mother_image_url, baby_result_url, 
        created time, comment, closed_at, complete,
        age, gender
    """

    __table_args__ = {'extend_existing': True}
    __tablename__ = "inference_result"

    id = Column(String, primary_key=True, index=True)
    
    father_url = Column(String)
    mother_url = Column(String)
    baby_url = Column(String)

    created_time = Column(DateTime, default=func.now())
    comment = Column(String)

    closed_at = Column(DateTime, default=None)
    complete = Column(Boolean, default=None)

    age = Column(String, default="None")
    gender = Column(String, default="None")

