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

import pytube
from pytube.cli import on_progress 
# import pytube ( get video from youtube link )
import views

@app.route('/detect', methods=['POST'])
def detect():
    
    Your_input = ''
    video_filename = ''

    # TODO : check file posted normally ( Local video file )
    if request.form['image_type'] == "1" :
        Your_input = request.files['file']
        video_filename=Your_input.filename
        gcp_control.upload_blob_file('teamg_images',Your_input,video_filename)
        video_path = 'https://storage.googleapis.com/teamg_images/'+video_filename
        views.video_insert('local',video_filename,video_path)

    # check URL posted normally ( Youtube or other video service )
    elif request.form['image_type'] == "0" :
        Your_input = request.form['image_url']
        print(Your_input)

        # if this url is youtube, use pytube module!
        Your_PyTube = pytube.YouTube(Your_input, on_progress_callback=on_progress)
        print(Your_PyTube.streams)
        video_filename = Your_PyTube.title
        
        # String 전처리
        #mylist = ['.', '`']
        video_filename = video_filename.replace(".", "")
        video_filename = video_filename.replace("'", "")


        # download youtube mp4 at our storage from youtube link
        temp_dir_path = './data/' 
        Your_PyTube.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first().download(temp_dir_path)
        

        # set input url to local path located in youtube mp4 file
        Your_input = temp_dir_path + video_filename + ".mp4"
        gcp_control.upload_blob_filename('teamg_images',Your_input,video_filename)
        os.remove(Your_input)
        video_path = 'https://storage.googleapis.com/teamg_images/'+video_filename
        views.video_insert('youtube',video_filename,video_path)

    

    # ( 공통 process ) upload video to gcp storage
    

    list_dir = ffmpeg.video_to_Img(video_path,video_filename)
                
    result = {}
    count=0
    censored_zero = 0
    censored_one = 0
    
    contents_id = views.get_video_id(video_filename)

    for filename in list_dir:
        count += 1
        location = video_path + '/' + filename
        detect_result = kakao_api.detect_adult(video_path + '/' + filename, 0)
        views.frame_insert(contents_id, location, filename, count*30000, detect_result)
        #eta = datetime.utcnow() + timedelta(seconds=2)
        #tasks.async_Add.apply_async(args=[video_filename, video_path + '/' + filename, count*30,detect_result], kwargs={},eta=eta)

        if detect_result == 0:
            censored_zero += 1
        else:
            censored_one += 1
                    
    result['over'] = censored_one / count
    result['under'] = censored_zero / count
    return {'result' : result }

