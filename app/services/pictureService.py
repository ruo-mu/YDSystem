import os
from typing import List
from fastapi import UploadFile, Depends

from app.models.user import User
from app.utils.authorize import authorize


class PictureService:
    def __init__(self):
        pass

    async def upload_picture(self, files: List[UploadFile]):
        try:
            upload_folder = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/uploaded_files'
            os.makedirs(upload_folder, exist_ok=True)
            for file in files:
                with open(upload_folder + f'/{file.filename}', 'wb+') as f:
                    f.write(await file.read())
            # return {"filename": file.filename}
        except Exception as e:
            return {"error": str(e)}

