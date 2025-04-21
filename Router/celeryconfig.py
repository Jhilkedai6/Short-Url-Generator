# Router/celeryconfig.py
from celery.schedules import crontab

beat_schedule = {
    'delete-every-5-mins': {
        'task': 'Router.tasks.delete_expire_url',  # Correct path and name
        'schedule': crontab(minute='*/5'),  # every 5 mins
    },
}

timezone = 'UTC'