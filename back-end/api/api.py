from fastapi import APIRouter

from api import predictor, gallery

router = APIRouter()
router.include_router(predictor.router, tags=["predictor"])
router.include_router(gallery.router, tags=["gallery"])
