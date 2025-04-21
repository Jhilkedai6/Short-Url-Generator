
from celery import Celery
from database import Session
from modle import ShortCode
from datetime import datetime
from . import celeryconfig  # Relative import
from modle import Url

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.config_from_object('Router.celeryconfig')  # Use full path for config

@celery_app.task
def delete_expire_url():
    db = Session()
    now = datetime.utcnow()
    
    deleted_count = db.query(ShortCode).filter(ShortCode.expire < now).first()

    long_url = db.query(Url).filter(Url.short_url == deleted_count.short_code).first()

    long_url.status = "expired"
    db.add(long_url)
    db.commit()

    db.delete(deleted_count)
    db.commit()
    db.close()
    print(f"[{now}] Deleted {deleted_count} expired URLs")