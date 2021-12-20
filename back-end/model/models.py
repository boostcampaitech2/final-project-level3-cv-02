from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

class Statistic(Base):
    __tablename__ = "statistic"

    avg_bounce_time = Column(Integer, primary_key=True)
    total_user = Column(Integer)
    avg_inference_time = Column(Integer)

class UserStatistic(Base):
    __tablename__ = "user_statistic"
    id = Column(Integer, primary_key=True)
    gender = Column(String)
    age = Column(Integer)
    rate = Column(Float)
    

class InferenceResult(Base):
    """
    id, father_image_url, mother_image_url, baby_result_url, created time, comment
    """

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

    # items = relationship("Item", back_populates="owner")


# class Item(Base):

#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")
