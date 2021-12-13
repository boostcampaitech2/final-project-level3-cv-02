import uvicorn
from api.api import router as api_router
# from core.config import API_PREFIX, DEBUG, PROJECT_NAME, VERSION
# from core.events import create_start_app_handler
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from typing import Callable
from dotenv import load_dotenv
import os
from api.s3 import *
#사람얽굴이 없나봐 ~ 다 셀카찍어서 한장씩 보내도록해 ~ 
def create_start_app_handler(app: FastAPI) -> Callable:
    def start_app() -> None:
        preload_model()

    return start_app


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(api_router)
    pre_load = False
    if pre_load:
        application.add_event_handler("startup", create_start_app_handler(application))
    return application


app = get_application()

if __name__ == "__main__":


    # access_key_id = os.getenv('access_key_ID')
    # access_key_pass = os.getenv('access_key_PASS')
    # s3 = s3_connection (access_key_id, access_key_pass)
    
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, debug=False)