import sys, os

os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
import models
from app import app, db


def add(video_name, imgdir, time, censored):
    input_img = models.img_upload(video_name, imgdir, time, censored)
    db.session.add(input_img)
    db.session.commit()

# def read():
#     return models.img_upload.query.count(), db.session.query(models.img_upload).all()