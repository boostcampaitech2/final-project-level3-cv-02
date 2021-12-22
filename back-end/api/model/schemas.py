from typing import List, Optional
from pydantic import BaseModel


class UserStatistic(BaseModel):
    id: int
    gender: str
    age: int
    rate: float


class Statistic(BaseModel):
    avg_bounce_time: int
    total_user: int
    avg_inference_time: int


class InferenceResultCreate(BaseModel):
    id: str
    father_url: str
    mother_url: str
    baby_url: str
    comment: str
    complete: bool
    closed_at: str
    created_time: str
    gender: str
    age: str
