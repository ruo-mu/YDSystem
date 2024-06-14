from typing import List
from fastapi import APIRouter, UploadFile, File, Depends
from app.models.user import User
from app.services.pictureService import PictureService
from app.utils.authorize import Authorize

authorize = Authorize()
router = APIRouter()
picture_service = PictureService()


@router.post('/upload_picture')
async def upload_picture(
        username: str = Depends(Authorize().get_current_user),
        files: List[UploadFile] = File(...),
):
    await picture_service.upload_picture(files)


@router.get('/match_key_points')
async def match_key_points():
    return picture_service.match_key_points()



