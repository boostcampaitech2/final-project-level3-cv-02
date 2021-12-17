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
    father_url: str
    mother_url: str

