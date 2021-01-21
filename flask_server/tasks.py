import sqlalchemy
import flask_celery
from celery.signals import task_postrun
from app import celery, db
import models
import views

@celery.task(bind=True)
def async_ReadMsg(self, img_type):
    imgtest = db.session.query(models.img_upload).get(img_type)
    imgtest.img_type = 'Changed_By_Celery'
    db.session.commit()

@celery.task(bind=True)
def async_Add(self, video_name, imgdir, time, censored):
    views.add(video_name, imgdir, time, censored)


@task_postrun.connect
def close_session(*args, **kwargs):
    db.session.remove()




# start celery worker
# celery -A tasks  worker --loglevel=info

# start celery beat
# celery -A tasks.celery beat --loglevel=info

celery.conf.beat_schedule = {
    'asyncReadMsg in every 10 seconds': {
        'task': 'asyncReadMsg',
        'schedule': 10.0
    },
}
