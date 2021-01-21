import os
from flask import Flask, request
from flask_cors import CORS
from function import kakao_api,ffmpeg
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
        file_path='././data/'+input_img_filename
        video_temp = 0
        # video 처리
        if input_img_filename.split('.')[-1] == 'mp4':
            if video_temp == 0:
                video_temp = 1
                res = ffmpeg.video_to_Img(file_path, input_img_filename)
                list_dir = []
                list_dir = os.listdir(res)
                
                result = {}
                count=0
                censored_zero = 0
                censored_one = 0
                
                for filename in list_dir:
                    count += 1
                    detect_result = kakao_api.detect_adult(res + '/' + filename, 1)
                    dbcon.add(input_img_filename,file_path,count*30,detect_result)
                    if detect_result == 0:
                        censored_zero += 1
                    else:
                        censored_one += 1
                    
                result['over'] = censored_one / count
                result['under'] = censored_zero / count
                print(result)
                return {'result' : detect_result}
        
        

    # elif request.form['image_type'] == "0":
    #     img_url = request.form['image_url']
    #     detect_result = kakao_api.detect_adult(img_url, 0)
    #     #dbcon.add('img_url',img_url)
    #     return {"result" : detect_result}

if __name__ == "__main__":
    app.run(debug=True)