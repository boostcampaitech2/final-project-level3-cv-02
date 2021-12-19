from fastapi import APIRouter

from api import predictor, gallery, dashboard

router = APIRouter()
router.include_router(predictor.router, tags=["predictor"])
router.include_router(gallery.router, tags=["gallery"])
router.include_router(dashboard.router, tags=["dashboard"])

