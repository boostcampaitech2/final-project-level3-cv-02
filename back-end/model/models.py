from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

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
    # items = relationship("Item", back_populates="owner")


# class Item(Base):

#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")
