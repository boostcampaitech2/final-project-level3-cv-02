import sys
import os
import shutil 
from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import HTMLResponse
from babygan import inference

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append("../")

from ..common.uploader import upload_image
from ..config.database import get_db
from ..service.inference_result import update_stop_inference, update_inference_fail, update_inference_result, create_inference_result

router = APIRouter()

@router.post("/cancle")
def cancel (
    body: dict
):
    uuid=body['uuid']
    db = get_db()
    db_false = update_stop_inference(db, uuid)
    db_false.complete = False  
    db.commit()
    crud.update_inference_fail (db=db, uuid=uuid)
    


@router.post("/uploadfiles" ) # 추후에 uploadfiles 이름 변경 -> predict
def predict(
    father_image: UploadFile = File(...),
    mother_image: UploadFile = File(...),
    uuid : str = Form(...),
    gender : str = Form(...),
    age : str = Form(...)
    ):
    """
    inference를 위한 함수입니다.
    Args:
        father_image : 사용자가 upload한 Father image file
        mother_image : 사용자가 upload한 Mother image file
    Return:
        baby_url : S3에서 추출한 결과물 url을 반환합니다.
    """
    setting_uuid = uuid #str(uuid.uuid4())
    
    father_url = upload_image(setting_uuid, father_image, "father")
    mother_url = upload_image(setting_uuid, mother_image, "mother")
    
    db = get_db()
    create_inference_result(db, inference_result = {"id":setting_uuid, "father_url":father_url, "mother_url":mother_url, "gender":gender, "age":age, "baby_url": None, "comment" : None, "complete": True }) 
    baby_file_path = inference.do_inference(father_url, mother_url, setting_uuid[:8]) 

    baby_url = upload_image(setting_uuid, baby_file_path, "baby")
    update_inference_result(db, setting_uuid, baby_url ) 
    if os.path.isdir(baby_file_path[:-12]): 
        print(baby_file_path[:-12])
        shutil.rmtree(baby_file_path[:-12])
    
    return { "baby_image_path": baby_url } # 요거 주석처리 한 것

@router.get("/")
def uploader():
    content = """
        <body>
            <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
                <input name="father_image" type="file">
                <input name="mother_image" type="file">
                <input type="submit">
            </form>
        </body>
    """
    return HTMLResponse(content=content)
