import os
from src import create_app
from src.celery_utils import make_celery

app = create_app()
celery = make_celery(app)
