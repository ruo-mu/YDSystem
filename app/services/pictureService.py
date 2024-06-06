import os

from fastapi import UploadFile


class PictureService:
    def __init__(self):
        pass

    async def upload_picture(self, file: UploadFile):
        pass
        try:
            os.makedirs('uploaded_files', exist_ok=True)
            with open(f'uploaded_files/{file.filename}', 'wb+') as f:
                f.write(await file.read())
            return {"filename": file.filename}
        except Exception as e:
            return {"error": str(e)}

