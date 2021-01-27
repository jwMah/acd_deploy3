import sys, os

os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
import models
from app import app, db


def video_insert(video_type, contents_name, location):
    video_temp = models.video_table(video_type, contents_name, location)
    db.session.add(video_temp)
    db.session.commit()

def frame_insert(contents_id, location, file_name, time_frame, ml_censored):
    frame_temp = models.img_table(contents_id, location, file_name, time_frame, ml_censored)
    db.session.add(frame_temp)
    db.session.commit()

def get_video_id(contents_name):
    return db.session.query(models.video_table.id).filter(models.video_table.contents_name == contents_name).first()
