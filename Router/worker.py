# Router/worker.py
from .tasks import celery_app
# Autodiscovery optional, only if you add more tasks in Router
celery_app.autodiscover_tasks(["Router"])