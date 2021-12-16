"""
import uvicorn
from api.api import router as api_router
# from core.config import API_PREFIX, DEBUG, PROJECT_NAME, VERSION
# from core.events import create_start_app_handler
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from typing import Callable

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

if __name__ == "__main__": # 
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, debug=False)
"""
import uvicorn
from api.api import router as api_router
# from core.config import API_PREFIX, DEBUG, PROJECT_NAME, VERSION
# from core.events import create_start_app_handler
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError 
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException 
from typing import Callable 
#
def create_start_app_handler(app: FastAPI) -> Callable: 
    def start_app() -> None: 
        preload_model()

    return start_app

def set_cors(application: FastAPI): # 아 아니다 로컬로 뜬다. ㅋㅋㅋㅋㅋ아냐아냐 ~ 
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
    uvicorn.run("main:app", host="0.0.0.0", port=6006 , reload=True, debug=False)
