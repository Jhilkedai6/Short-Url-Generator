from fastapi import APIRouter, HTTPException, Depends, Query
from starlette import status
from database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
import requests
from .code import return_short_url
from modle import Url
from datetime import datetime
from .auth import get_current_user
from modle import User, Logs
from rate_limitter import limiter
from fastapi import Request

router = APIRouter(
    prefix="/admin",
    tags=['Admin']
)


db_dpendiencies = Annotated[Session, Depends(get_db)]
user_dependiencies = Annotated[dict, Depends(get_current_user)]



@router.put("/Be_Admin/")
@limiter.limit("1/second")
async def be_admin(request: Request, user: user_dependiencies, db: db_dpendiencies, Admin_Code: int = Query(...)):

    """ Be admin by entering admin code"""

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if Admin_Code != 69:
        return "Admin Code not valid"
    
    user_info = db.query(User).filter(User.email == user.get("email")).first()

    if user_info.role == "admin":
        return "You are admin already"
    
    user_info.role = "admin"
    
    db.add(user_info)
    db.commit()

    log = Logs(
        email=user_info.email,
        username=user_info.username,
        activity="Become Admin",
        time=datetime.utcnow()
    )
    db.add(log)
    db.commit()


    return "You are admin now "
    


@router.get("/All_USer")
@limiter.limit("1/second")
async def all_user(request: Request, db: db_dpendiencies, user: user_dependiencies):
    """ Gets all user """

    if not user or not user.get("role") == "admin":
        raise HTTPException(status_code=401, detail="Unauthorized")

    users = db.query(User).all()

    return users



@router.delete("/delete_user/")
@limiter.limit("1/second")
async def delete_acc(request: Request, user: user_dependiencies, db: db_dpendiencies, Email: str = Query(..., title="Email to delete")):

    """ Delete user"""

    if not user or not user.get("role") ==  "admin":
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_info = db.query(User).filter(User.email == Email).first()
    if not user_info:
        raise HTTPException(status_code=404, detail="User not found with this email")
    
    db.delete(user_info)
    db.commit()


    log = Logs(
        email=user_info.email,
        username=user_info.username,
        activity=f"Acc deleted email: {Email}",
        time=datetime.utcnow()
    )
    db.add(log)
    db.commit()

    return "User has been successfully deleted"


@router.get("/Logs")
@limiter.limit("1/second")
async def all_logs(request: Request, db: db_dpendiencies, user: user_dependiencies):

    """ Returns all the logs of admin"""

    if not user or not user.get("role") ==  "admin":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    log = db.query(Logs).all()

    return log









    