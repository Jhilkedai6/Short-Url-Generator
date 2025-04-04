from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os 


# URL = "postgresql://postgres:9800@localhost:5432/ShortUrl" # put in env

URL = "sqlite:///url.db"
Engine = create_engine(url=URL, connect_args={"check_same_thread": False})
Session = sessionmaker(autoflush=False, autocommit=False, bind=Engine)

Base = declarative_base()


def get_db(): 
    """ retrive database and close it """
    db = Session()

    try:
        yield db
    finally:
        db.close()
