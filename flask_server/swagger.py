# 필요한 모듈을 불러온다
from flask import Flask, request
from app import app
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask_restplus import Api, Resource, fields
from function import kakao_api

# app = Flask(__name__) # Flask App 생성한다
api = Api(app, version='1.0', title='Adult Contents Detector API', description='성인 컨텐츠 detect API입니다') # API 만든다
ns  = api.namespace('detect', description='성인 컨텐츠 detect') # /detect/ 네임스페이스를 만든다

# REST Api에 이용할 데이터 모델을 정의한다
model_contents = api.model('row_contents', {
    'image_url': fields.String(required=True, description='이미지 url', help='이미지 url은 필수'),
    'image_type': fields.Integer(required=True, description='이미지 type', help='이미지 type은 필수'),
    'result' : fields.String(readOnly=True, description='detect result', help='')
})

@ns.route('/') # 네임스페이스 x.x.x.x/detect 하위 / 라우팅
class ContentsDetector(Resource):
    @ns.expect(model_contents)
    @ns.marshal_with(model_contents, code=201)
    def post(self):
        '''새로운 컨텐츠를 detect한다'''

        api.payload['result'] = kakao_api.detect_adult(api.payload['image_url'],api.payload['image_type'])

        # request.json[파라미터이름]으로 파라미터값 조회할 수 있다
        print('result', request.json['result'])
        return api.payload['result'], 201
