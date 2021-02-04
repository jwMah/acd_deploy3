import sys, os
from flask import Flask, request, Blueprint
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
config.read('./config.ini')
app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
celery = make_celery(app)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = config['DEFAULT']['SQLALCHEMY_DATABASE_URI']
# 추가하지 않을 시 FSADeprecationWarning 주의가 떠서 추가해 줌
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Blueprint('api',__name__)


import tasks
# import dbcon

import pytube
from pytube.cli import on_progress 
# import pytube ( get video from youtube link )
import views

video_id = 0
video_filename = ''
video_path= ''
video_path_signed = ''
video_type = ''
#list_dir = []
img_count = 1
    
@api.route('/videoUploading', methods=['POST'])
def videoUploading():
    global video_id
    Your_input = ''
    global video_filename
    global video_path
    global video_path_signed
    global video_type

    # TODO : check file posted normally ( Local video file )
    if request.form['image_type'] == "1" :
        Your_input = request.files['file']
        video_filename=secure_filename(Your_input.filename)
        Your_input.save(os.path.join('./data/',video_filename))
        gcp_control.upload_blob_filename('teamg-data','./data/'+video_filename,video_filename)
        video_path = 'https://storage.googleapis.com/teamg-data/'+video_filename
        video_path_signed = gcp_control.generate_download_signed_url_v4('teamg-data', video_filename)
        os.remove('./data/'+video_filename)
        video_type = 'local'
        # views.video_insert('local',video_filename,video_path)
        eta = datetime.utcnow() + timedelta(seconds=2)
        tasks.async_video_insert.apply_async(args=['local',video_filename,video_path], kwargs={},eta=eta)

    # check URL posted normally ( Youtube or other video service )
    elif request.form['image_type'] == "0" :
        Your_input = request.form['image_url']
        print(Your_input)

        # if this url is youtube, use pytube module!
        Your_PyTube = pytube.YouTube(Your_input, on_progress_callback=on_progress)

        # download youtube mp4 at our storage from youtube link
        temp_dir_path = './data/' 
        Your_PyTube.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first().download(temp_dir_path)
        # get video filename from local storage
        video_filename = os.listdir(temp_dir_path)
        video_filename.remove('.keep')
        video_filename = video_filename[0]
        video_filename = video_filename[0:-4]

        # set input url to local path located in youtube mp4 file
        Your_input = temp_dir_path + video_filename
        # upload video to google storage
        gcp_control.upload_blob_filename('teamg-data',Your_input+'.mp4',video_filename)
        # remove video file at local storage
        os.remove(Your_input+'.mp4')
        # url of video from google storage
        video_path = 'https://storage.googleapis.com/teamg-data/'+video_filename
        # get signed url of video from google storage
        video_path_signed = gcp_control.generate_download_signed_url_v4('teamg-data', video_filename)
        eta = datetime.utcnow() + timedelta(seconds=2)
        tasks.async_video_insert.apply_async(args=['youtube',video_filename, video_path], kwargs={},eta=eta)
        #views.video_insert('youtube',video_filename,'https://storage.googleapis.com/teamg-data/'+video_filename)
        views.get_video_id()
        video_type = 'youtube'

    return {'video_filename' : video_filename }


@api.route('/frameUploading', methods=['POST'])
def frameUploading():
    #global list_dir
    global video_filename
    global video_path
    global video_path_signed
    global img_count
    print(img_count)
    views.get_path_by_id(id)
    # ( 공통 process ) upload frames to gcp storage
    img_count = ffmpeg.video_to_Img(video_path_signed,video_filename)
    print(img_count)
    # video filename, frame 갯수
    result = {}
    result['video_filename'] = video_filename
    result['frame_counts'] = img_count
    return {'result' : result}


@api.route('/detectFinal', methods=['POST'])
def detectFinal(): 
    global video_id
    global video_filename
    global video_path
    global video_path_signed
    global video_type
    #global list_dir
    global img_count

    # insert contents analysis to DB
    result = {}
    censored_G = 0
    censored_PG = 0
    censored_R = 0
    count = 1
    video_id = views.get_video_id(video_filename)
    #
    print(img_count)
    for num in range(img_count):
        detect_result = kakao_api.detect_adult(video_path+'/'+'frm-'+ str(count-1) +'.jpg', 0)
        views.frame_insert(int(video_id[0]), video_path +'/'+'frm-'+ str(count-1)+'.jpg', 'frm-'+ str(count-1)+'.jpg', count*30000-15000, detect_result)
        count = count + 1

        if detect_result == 'G':
            censored_G = censored_G + 1
        elif detect_result == 'PG':
            censored_PG = censored_PG + 1
        else:
            censored_R = censored_R + 1

    pct_PG = censored_PG / img_count
    pct_R = censored_R / img_count
    if pct_R==0 and pct_PG <= 0.2:
        censored = 'G'
    elif pct_R <= 0.2:
        censored = 'PG'
    else:
        censored = 'R'
    result['censored'] = censored
    #views.video_censored(int(video_id[0]), censored)
    eta = datetime.utcnow() + timedelta(seconds=2)
    tasks.async_video_censored.apply_async(args=[int(video_id[0]), censored], kwargs={},eta=eta)

    # get Video Access URL from GCP storage
    result['video_URL'] = video_path_signed
    print(result)


    return {'result' : result }

####### detect.js reply ########


# read contents analysis from DB
@api.route('/frame', methods=['POST'])
def readdb():
    global video_id
    global video_filename
    contents_analysis = views.frame_read(video_id)

    img_dict={}
    idx = 0
    for id, location, time_frame, ml_censored in contents_analysis:
        img={}
        img['id'] = id
        img['location'] = gcp_control.generate_download_signed_url_v4('teamg-data', video_filename + '/frm-' + str(idx) + '.jpg')
        img['time_frame'] = time_frame
        img['ml_censored'] = ml_censored

        img_dict[idx]=img
        idx += 1

    return {'img_dict' : img_dict }

#바뀐 frame censored와 video censored 업데이트 request 처리
@api.route('/update', methods=['POST'])
def update():
    changed_lists = request.get_json(force=True)

    count = 0
    for changed_img in changed_lists:
        if changed_img['id'] == 0:
            if changed_img['censored'] == '19세 이용가':
                censored = 'R'
            elif changed_img['censored'] == '15세 이용가':
                censored = 'PG'
            else:
                censored = 'G'
            eta = datetime.utcnow() + timedelta(seconds=2)
            tasks.async_video_update.apply_async(args=[video_id[0], censored], kwargs={},eta=eta)
        else:
            print('sibal')
            eta = datetime.utcnow() + timedelta(seconds=2)
            tasks.async_frame_update.apply_async(args=[changed_img['id'], changed_img['censored']], kwargs={},eta=eta)
        
        count = count+1
    return {'changed_count' : count}


app.register_blueprint(api, url_prefix='/api')

