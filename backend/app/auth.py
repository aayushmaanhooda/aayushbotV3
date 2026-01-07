from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, Request, Response
from sqlmodel import Session, select
from models import User
from uuid import UUID
from dotenv import load_dotenv
import os
import types


load_dotenv()

expire_time = os.getenv("EXPIRE_TIME")
secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
cookie_name = os.getenv("COOKIE_NAME", "access_token")

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="admin", auto_error=False)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
    response: Response | None = None,
):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        minutes = int(expire_time) if expire_time else 60
        expire = datetime.now() + timedelta(minutes=minutes)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)

    # If a Response is provided, store session in an HttpOnly cookie.
    if response is not None:
        # Local dev is usually http://, so default to samesite=lax + secure=false.
        # In production, override with COOKIE_SAMESITE=none and COOKIE_SECURE=true if needed.
        cookie_samesite = os.getenv("COOKIE_SAMESITE", "lax").lower()
        cookie_secure = os.getenv("COOKIE_SECURE")
        secure = (
            (cookie_secure.lower() == "true") if cookie_secure is not None else False
        )

        response.set_cookie(
            key=cookie_name,
            value=encoded_jwt,
            httponly=True,
            secure=secure,
            samesite=cookie_samesite,  # "lax" | "strict" | "none"
            max_age=int(os.getenv("COOKIE_MAX_AGE", "3600")),
            path="/",
        )

    return encoded_jwt


def authenticate_user(db: Session, username: str, password: str):
    user = db.exec(select(User).where(User.username == username)).first()

    if not user:
        return False

    if not verify_password(password, user.hash_password):
        return False

    return user


# use this fucntion sfor all protected routs now
def get_current_user(request: Request, token: str | None = Depends(oauth_2_scheme)):
    # Prefer HttpOnly cookie storage, but still allow Authorization header for tooling.
    raw_token = token or request.cookies.get(cookie_name)
    if not raw_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        payload = jwt.decode(raw_token, secret_key, algorithms=[algorithm])
        user_id: str = payload.get("sub")

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    return user_id
