from datetime import datetime, timedelta

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.models.token import Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


class Authorize:
    SECRET_KEY = "8904626d85b06fe350364741aaa3b05e96586dc1ace8888dea5206b8d303e151"
    ALGORITHM = "HS256"

    def __init__(self):
        pass

    def create_access_token(self, data: str, expires_delta: int = 60 * 24 * 1) -> Token:
        token_expires = datetime.utcnow() + timedelta(minutes=expires_delta)
        token_data = {
            "sub": data,
            "exp": token_expires
        }
        token = jwt.encode(token_data, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return Token(access_token=token, token_type="bearer")

    def get_current_user(self, token: str = Depends(oauth2_scheme)) -> str:
        exp = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=self.ALGORITHM)
            username: str = payload.get("sub")
            if username is None:
                raise exp
        except JWTError:
            raise exp
        return username


authorize = Authorize()
