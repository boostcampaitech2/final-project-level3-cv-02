from typing import List, Optional
from pydantic import BaseModel

class InferenceResultBase(BaseModel):
    father_url: str
    mother_url: str


class InferenceResult(InferenceResultBase):
    baby_url: str
    class Config:
        orm_mode = True


class InferenceResultCreate(InferenceResultBase):
    id: str
    father_url: str
    mother_url: str
    baby_url: str
    comment: str
    complete: bool
    closed_at: str 
    created_time : str 
    gender : str
    age : str 