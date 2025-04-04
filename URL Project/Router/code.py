import random
import string
from modle import ShortCode
from sqlalchemy.orm import Session

def create_short_url() -> str:
    """Generates a random 6-character short URL"""
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for _ in range(6))

def return_short_url(db: Session) -> str:
    """Generates a unique short URL and stores it in the database"""

    while True:  # Keep generating until a unique short URL is found
        short_url = create_short_url()
        is_same = db.query(ShortCode).filter(ShortCode.short_code == short_url).first()

        if is_same is None:  # If the short URL does not exist, save it
            store = ShortCode(short_code=short_url)
            
            db.add(store)
            db.commit()

            return short_url