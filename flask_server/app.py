import os
from flask import Flask, request
from flask_cors import CORS
from function import kakao_api
from werkzeug.utils import secure_filename
import configparser
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


config = configparser.ConfigParser()
config.read('../config.ini')
app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = config['DEFAULT']['SQLALCHEMY_DATABASE_URI']
# 추가하지 않을 시 FSADeprecationWarning 주의가 떠서 추가해 줌
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


import dbcon
@app.route('/detect', methods=['POST'])
def detect():
    if request.form['image_type'] == "1" :
        input_img = request.files['file']
        input_img_filename = secure_filename(input_img.filename)
        input_img.save(os.path.join('./data/', input_img_filename))
        detect_result = kakao_api.detect_adult('./data/'+input_img_filename, 1)
        dbcon.add('img_file','/flask_server/data/'+input_img_filename)
        return {'result' : detect_result}

    elif request.form['image_type'] == "0":
        img_url = request.form['image_url']
        detect_result = kakao_api.detect_adult(img_url, 0)
        dbcon.add('img_url',img_url)
        return {"result" : detect_result}
