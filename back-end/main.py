
import uvicorn
from api.api import router as api_router
# from core.config import API_PREFIX, DEBUG, PROJECT_NAME, VERSION
# from core.events import create_start_app_handler
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError 
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException 
from typing import Callable 


from model import models
from model.models import Base
from model.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

def create_start_app_handler(app: FastAPI) -> Callable: 
    def start_app() -> None: 
        preload_model()

    return start_app

def set_cors(application: FastAPI): 
    origins = ["*" ]
    application.add_middleware( CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"], )

def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(api_router)
    pre_load = False
    if pre_load:
        application.add_event_handler("startup", create_start_app_handler(application))
    set_cors(application)
    return application

app = get_application()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=6006 , reload=True, debug=False, workers=4)
