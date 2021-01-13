from flask import Flask, request
from flask_cors import CORS
from function import kakao_api
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app)

@app.route('/detect', methods=['POST'])
def detect():
    if request.form['image_type'] == "1" :
        input_img = request.files['file']
        input_img_filename = secure_filename(input_img.filename)
        print(input_img)
        input_img.save(os.path.join('./data/', input_img_filename))
        detect_result = kakao_api.detect_adult('./data/'+input_img_filename, 1)
        return {'result' : detect_result}
    elif request.form['image_type'] == "0":
        img_url = request.form['image_url']
        detect_result = kakao_api.detect_adult(img_url, 0)
        return {"result" : detect_result}
    '''
    if img_url != "":
        detect_result = test_kakao.detect_adult(img_url, 0)
        return {"result" : "detect_result"}
        
    elif client_img != "":
            img_filename = secure_filename(client_img.filename)
            client_img.save(os.path.join('./flask_server/data/', img_filename))
            detect_result = test_kakao.detect_adult('./flask_server/data/'+img_filename, 1)
            return {"result" : "detect_result"}
    '''


    