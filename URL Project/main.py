from Router import crud
from modle import Url
from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
from fastapi import Depends, FastAPI
import modle 
from database import Engine
from modle import ShortCode

app = FastAPI()
modle.Base.metadata.create_all(Engine)

db_dpendiencies = Annotated[Session, Depends(get_db)]

app.include_router(crud.router)


@app.get("/test")
async def test(db: db_dpendiencies):

    test = db.query(Url).all()
    return test