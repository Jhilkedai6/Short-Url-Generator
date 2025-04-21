from typing import Annotated
from database import Engine
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from modle import Url
from redis import Redis
from database import get_db
import httpx
from Router import crud, auth, admin
from starlette import status
from fastapi import HTTPException
from modle import ShortCode
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from slowapi.util import get_remote_address
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
import modle
from fastapi import Request
from rate_limitter import limiter


modle.Base.metadata.create_all(Engine)




app = FastAPI()

app.include_router(auth.router)
app.include_router(crud.router)
app.include_router(admin.router)


app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def ratelimit_handler(request: Request, exc: RateLimitExceeded):

    return JSONResponse(
        status_code=HTTP_429_TOO_MANY_REQUESTS,
        content={"error": "Too many requests, slow down!"},
    )



# Database dependencies
db_dependencies = Annotated[Session, Depends(get_db)]


@app.on_event("startup")
async def startup_event():

    app.state.redis = Redis(host="localhost", port=6379)
    app.state.http_client = httpx.AsyncClient()
    print("Startup completed successfully")


@app.on_event("shutdown")
async def shutdown_event():

    app.state.redis.close()
    print("Close")



# Test endpoint to check if database is working
@app.get("/test")
@limiter.limit("1/second")
async def test(request: Request, db: db_dependencies):
    test_data = db.query(Url).all()  # Query all Urls
    return test_data


def store_redis(short_url: str, long_url: str, db: Session):
    
    cached_url = app.state.redis.get(short_url)
    if not cached_url:
        app.state.redis.set(short_url, long_url)
    
    get_url = db.query(Url).filter(Url.long_url == long_url).first()
    get_url.access_count += 1
    db.add(get_url)
    db.commit()
    
    return long_url



@app.get("/shorten/", status_code=status.HTTP_200_OK)
@limiter.limit("1/second")
async def get_url(request: Request, db: db_dependencies, short_url: str):
    """ Fetch long url with short url and return it """
    

    get_url = db.query(Url).filter(Url.short_url == short_url).first()

    if not get_url:
        raise HTTPException(status_code=404, detail="Invalid Short Url")
    
    access_count = get_url.access_count
    long_url = get_url.long_url #Long url

    if access_count < 5:

        get_url.access_count = get_url.access_count + 1 # every time user use short url add it to access_count

        db.add(get_url)
        db.commit()

        return long_url #return long_url
    
    store_redis(short_url=short_url, long_url=long_url, db=db)
    return long_url



