from fastapi import APIRouter

from api import predictor, uploader

router = APIRouter()
router.include_router(predictor.router, tags=["predictor"])
router.include_router(uploader.router, tags=["uploader"])
