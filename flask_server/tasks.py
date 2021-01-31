import sqlalchemy
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
def async_video_insert(self, video_type, contents_name, location):
    views.video_insert(video_type, contents_name, location)

@celery.task(bind=True)
def async_frame_insert(self, contents_id, location, file_name, time_frame, ml_censored):
    views.frame_insert(contents_id, location, file_name, time_frame, ml_censored)

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
