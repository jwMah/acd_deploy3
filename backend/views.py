import sys, os
from sqlalchemy import sql
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

def frame_read(video_id):
    return db.session.query(models.img_table.id,models.img_table.location,models.img_table.time_frame,models.img_table.ml_censored).filter(models.img_table.contents_id == video_id).all()


def frame_update(frame_id, admin_censored):
    temp = db.session.query(models.img_table).filter(models.img_table.id==frame_id).first()
    temp.admin_censored = admin_censored
    temp.update_time = sql.func.now()
    db.session.commit()

def video_censored(video_id, censored):
    temp = db.session.query(models.video_table).filter(models.video_table.id==video_id).first()
    temp.censored = censored
    db.session.commit()

def video_update(video_id, censored):
    temp = db.session.query(models.video_table).filter(models.video_table.id==video_id).first()
    temp.censored = censored
    temp.update_time = sql.func.now()
    db.session.commit()