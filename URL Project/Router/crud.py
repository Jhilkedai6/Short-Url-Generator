from fastapi import APIRouter, HTTPException, Depends, Query
from starlette import status
from database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
import requests
from .code import return_short_url
from modle import Url
from datetime import datetime

router = APIRouter()


db_dpendiencies = Annotated[Session, Depends(get_db)]

def check_url(Url: str):
    """ Url validation check """

    try:
        response = requests.get(url=Url, timeout=5)
    except requests.RequestException:
        raise HTTPException(status_code=400, detail="Url not correct")

    return True


@router.post("/Make_Short_Url/", status_code=status.HTTP_201_CREATED)
async def make_short_url(db: db_dpendiencies, url: str = Query(...)):
    """ Create short code to access long url"""

    is_url_correct = check_url(Url=url) # check url

    if is_url_correct:
        short_url = return_short_url(db)

        store_url = Url(
            long_url=url,
            short_url=short_url,
            created_date=datetime.utcnow(),
            updated_date=datetime.utcnow()
        )
        db.add(store_url) #add url to db
        db.commit()


@router.get("/shorten/", status_code=status.HTTP_200_OK)
async def get_url(db: db_dpendiencies, short_url: str):
    """ Fetch long url with short url and return it """
    

    get_url = db.query(Url).filter(Url.short_url == short_url).first()

    if not get_url:
        raise HTTPException(status_code=404, detail="Invalid Short Url")
    
    long_url = get_url.long_url #Long url
    
    if get_url.access_count is None: #check if it is none is none assign it 0
        get_url.access_count = 0

    get_url.access_count = get_url.access_count + 1 # every time user use short url add it to access_count

    db.add(get_url)
    db.commit()

    return long_url #return long_url



@router.put("/Update_url/", status_code=status.HTTP_200_OK)
async def update_url(db: db_dpendiencies, short_url: str = Query(...), updated_url: str = Query(...)):
    """ Fetch Long url with short url and Update it """

    is_url_correct = check_url(Url=updated_url)

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
async def delete_url(db: db_dpendiencies, short_url: str):
    """Fetch long url with short url and delete"""


    get_url = db.query(Url).filter(Url.short_url == short_url).first()

    if not get_url:
        raise HTTPException(status_code=404, detail="Invalid Short Url")
    
    db.delete(get_url)
    db.commit()

    return "Url has been deleted"


        
