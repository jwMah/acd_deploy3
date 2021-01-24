import sys, os
from flask import Flask, request
from flask_cors import CORS
from function import kakao_api, ffmpeg
from werkzeug.utils import secure_filename
import configparser
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from datetime import timedelta
from flask_celery import make_celery
from function import gcp_control


config = configparser.ConfigParser()
config.read('../config.ini')
app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
celery = make_celery(app)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = config['DEFAULT']['SQLALCHEMY_DATABASE_URI']
# 추가하지 않을 시 FSADeprecationWarning 주의가 떠서 추가해 줌
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

import tasks
# import dbcon
@app.route('/detect', methods=['POST'])
def detect():
    # TODO : check file posted normally
    if request.form['image_type'] == "1" :
        input_video = request.files['file']
        video_filename=input_video.filename

        # upload video to gcp storage
        gcp_control.upload_blob_file('teamg_images',input_video,input_video.filename)
        video_path = 'https://storage.googleapis.com/teamg_images/'+video_filename

        list_dir = ffmpeg.video_to_Img(video_path,video_filename)
                
        result = {}
        count=0
        censored_zero = 0
        censored_one = 0
                
        for filename in list_dir:
            count += 1
            print(video_path + '/' + filename)
            detect_result = kakao_api.detect_adult(video_path + '/' + filename, 0)
            eta = datetime.utcnow() + timedelta(seconds=2)
            tasks.async_Add.apply_async(args=[video_filename, video_path + '/' + filename, count*30,detect_result], kwargs={},eta=eta)

            if detect_result == 0:
                censored_zero += 1
            else:
                censored_one += 1
                    
        result['over'] = censored_one / count
        result['under'] = censored_zero / count
        return {'result' : result }
