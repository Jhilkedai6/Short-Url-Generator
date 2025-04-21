from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from pydantic import BaseModel
from modle import User
from datetime import datetime
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, ExpiredSignatureError, JWTError
from datetime import timedelta

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


db_dpendencies = Annotated[Session, Depends(get_db)]
bcrypt = CryptContext(schemes=['bcrypt'])

Screate = "0812d837da9698c7c660708d552b3d1b2d74485d921416146cba7b0bae7342cf"
Algorithm = "HS256"

oauth = OAuth2PasswordBearer(tokenUrl="/auth/token")


class AccModel(BaseModel):

    email: str
    username: str
    password: str


def check_user(model_username: str, model_password: str, db: Session) -> User:
    """ Check username and password and return user"""
    
    user = db.query(User).filter(User.username == model_username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found with this username")
    
    if not bcrypt.verify(model_password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    return user

def create_jwt(role: str, email: str, username: str, expire_delta: timedelta) -> str:
    """ Create jwt token and return it"""

    expire_time = datetime.utcnow() + expire_delta
    encode = {
        "email": email,
        "username": username,
        "role": role,
        "exp": expire_time
    }

    return jwt.encode(encode, Screate, algorithm=Algorithm)


async def get_current_user(token: Annotated[str, Depends(oauth)]) -> dict:
    """ Decode jwt token and retrive user data """

    try:
        payload = jwt.decode(token, Screate, algorithms=Algorithm)
        email = payload.get("email")
        username = payload.get("username")
        role = payload.get("role")

        data = {
            "email": email,
            "username": username,
            "role": role

        }
        return data
    except ExpiredSignatureError:
        return "Jwt token has been expired"
    
    except JWTError:
        return "Incorrect Jwt token"


@router.post("/Sing-up")
async def singup(db: db_dpendencies, model: AccModel) -> str:
    """create user account"""

    if model.username == "string" or model.password == "string" or model.email == "string":
        raise HTTPException(status_code=400, detail="Singup field shouldnot be empty")


    user_info = User(
        email=model.email,
        username=model.username,
        password=bcrypt.hash(model.password),
        acc_created=datetime.utcnow(),
        role="user"

    )
     
    db.add(user_info)
    db.commit()

    return "User acc has been created successfully"


@router.post("/token")
async def login(db: db_dpendencies, login_info: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict:
    """ Retrurn jwt token in format """

    user = check_user(login_info.username, login_info.password, db)

    jwt = create_jwt(user.role, user.email, user.username, timedelta(minutes=30))

    return {"access_token": jwt, "token_type": "bearer"}

