from typing import List

from fastapi import APIRouter, UploadFile, File, Depends

from app.services.pictureService import PictureService
from app.utils.authorize import Authorize

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")
authorize = Authorize()
# router = APIRouter(dependencies=[Depends(authorize.get_current_user)])
router = APIRouter()
picture_service = PictureService()


@router.post('/upload_picture')
async def upload_picture(
        # user: User = Depends(Authorize().get_current_user),
        files: List[UploadFile] = File(...),
):
    await picture_service.upload_picture(files)


