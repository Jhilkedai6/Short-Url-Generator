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
from datetime import timedelta
from modle import User, ShortCode
from fastapi import Request
from rate_limitter import limiter


router = APIRouter(
    prefix="/url",
    tags=['URL']
)


db_dpendiencies = Annotated[Session, Depends(get_db)]
user_dependiencies = Annotated[dict, Depends(get_current_user)]

def check_url(Url: str):
    """ Url validation check """

    try:
        response = requests.get(url=Url, timeout=5)
    except requests.RequestException:
        raise HTTPException(status_code=400, detail="Url not correct")

    return True


@router.post("/Make_Short_Url/", status_code=status.HTTP_201_CREATED)
@limiter.limit("1/second")
async def make_short_url(request: Request, user: user_dependiencies, db: db_dpendiencies, url: str = Query(...), Expire_time: int = Query(..., description="Input expire time in days")):
    """ Create short code to access long url"""

    if not user:
        raise HTTPException(status_code=401, detail="Not Authorized")
    is_url_correct = check_url(Url=url) # check url

    user_info = db.query(User).filter(User.email == user.get("email")).first()

    if is_url_correct:
        short_url = return_short_url(db, Expire_time)

        store_url = Url(
            long_url=url,
            short_url=short_url,
            created_date=datetime.utcnow(),
            updated_date=datetime.utcnow(),
            expire_time=datetime.utcnow() + timedelta(minutes=Expire_time),
            status="Active",
            user_id=user_info.id
        )
        db.add(store_url) #add url to db
        db.commit()

        return short_url
    

@router.get("/Get_Short")
@limiter.limit("1/second")
def get_short(request: Request, user: user_dependiencies, db: db_dpendiencies):

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    shorts = db.query(ShortCode).filter()
    return shorts




@router.put("/Update_url/", status_code=status.HTTP_200_OK)
@limiter.limit("1/second")
async def update_url(request: Request, user: user_dependiencies, db: db_dpendiencies, short_url: str = Query(...), updated_url: str = Query(...)):
    """ Fetch Long url with short url and Update it """

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    is_url_correct = check_url(Url=updated_url)  #check url

    if is_url_correct:

        is_url = db.query(Url).filter(Url.short_url == short_url).first()

        if not is_url:
            raise HTTPException(status_code=404, detail="Invalid Short Url")
        
        is_url.long_url = updated_url
        is_url.updated_date = datetime.utcnow()

        db.add(is_url)
        db.commit()

        return "Url has been scuessfully updated"
    

@router.delete("/Delete_Url/", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("1/second")
async def delete_url(request: Request, user: user_dependiencies, db: db_dpendiencies, short_url: str):
    """Fetch long url with short url and delete"""

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")


    get_url = db.query(Url).filter(Url.short_url == short_url).first()

    if not get_url:
        raise HTTPException(status_code=404, detail="Invalid Short Url")
    
    db.delete(get_url)
    db.commit()

    return "Url has been deleted"


