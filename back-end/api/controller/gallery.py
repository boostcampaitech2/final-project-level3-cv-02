import shutil
from fastapi import APIRouter

import sys
import os

sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
)
sys.path.append("../")

from ..config.database import get_db
from ..service.inference_result import (
    get_inference_results,
    update_comment,
)

router = APIRouter()


@router.get("/gallery")
def get_image_url():
    """
    gallery에 표시될 이미지 url을 반환합니다.
    Return:
        list : father_url, mother_url, baby_url을 담은 list 반환
    """
    urls = []
    db = get_db()
    users = get_inference_results(db)
    for i, user in enumerate(users):
        if user.comment:
            urls.append(
                {
                    "father_url": user.father_url,
                    "mother_url": user.mother_url,
                    "baby_url": user.baby_url,
                    "comment": user.comment,
                }
            )
    return urls


@router.post("/share")
def share_image(body:dict):
    """
    이미지를 공유할 때 사용자가 작성한 comment를 db에 업데이트합니다.
    Args: 
        body['uuid']: comment를 작성한 사용자의 uuid 
        body['comment']: 사용자가 작성한 comment
    """
    uuid = body['uuid']
    comment = body['comment']
    db = get_db()
    update_comment(db, uuid, comment)
