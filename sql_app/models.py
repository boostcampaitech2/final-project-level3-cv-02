from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base

class InferenceResult(Base):
    """
    id, father_image_url, mother_image_url, baby_result_url, created time, comment
    """

    __tablename__ = "inference_result"

    id = Column(Integer, primary_key=True, index=True)
    
    father_url = Column(String, unique=True)
    mother_url = Column(String, unique=True)
    baby_url = Column(String, unique=True)

    created_time = Column(DateTime)
    comment = Column(String)
    # items = relationship("Item", back_populates="owner")


# class Item(Base):

#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")
