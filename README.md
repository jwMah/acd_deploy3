## 프로젝트 설명
성인 유해 컨텐츠 판별 Web Application입니다.  
사용자가 입력한 동영상의 프레임을 추출하여 ai를 이용해 유해한 컨텐츠인지 아닌지를 판별합니다.

### 사용 기술
이 프로젝트는 React.js 라이브러리를 통해 제작되며, API 서버는 Flask프레임워크를 사용합니다. 
또한 비동기처리를 위한 RabbitMQ와 Celery를 부가적으로 사용합니다. 
Database로는 gcp의 PostgreSQL instance를 사용하여 연동합니다.  

- React.js
- Flask
- RabbitMQ
- Celery
- GCP PostgreSQL

### design doc
https://www.notion.so/Design-Doc-_-0120-8ac2c8e842a8429fb169b21372554dd1

### AI Model
CNN(Convolutional Neural Network)

## Getting Started
```sh
git clone https://github.com/2021-Sillicon-Valley-Internship-TeamG/Adult_Contents_Detector.git
npm install                                           # 의존성 파일 설치

# Then:
cd flask_server/
celery -A app.celery worker --loglevel=info           # for rabbitMQ
FLASK_APP = swagger.py flask run -h 0.0.0.0 -p 9991   # for swagger (0.0.0.0:9991)
flask run
cd ../
npm run start
```

### Swagger
<img width="550px" height="300px" src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FVoAuD%2FbtqUf0TF603%2FuPaEWbmyRicseGoNRLtpsk%2Fimg.png"></img>

### RabbitMQ
<img width="550px" height="300px" src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FupCAF%2FbtqUhzVOUBF%2F78efHoKKCXevEf8WgrAdNK%2Fimg.png"></img>

## Directory Structure
```bash
├── README.md                 - 리드미 파일
│
├── flask_server/             - 백엔드 플라스크 디렉토리
│   ├── app.py                - 서버 시작, 서버 api reply 처리
│   ├── dbcon.py              - 디비 컨트롤러 파일
│   ├── flask_celery.py       - celery 생성 파일
│   ├── task.py               - queue 적재 task 생성 파일
│   ├── models.py             - 디비 모델 파일
│   ├── swagger.py            - swagger 실행 파일
│   ├── models.py             - 디비 모델 파일
│   │
│   ├── data/                 - 백엔드 동영상, 이미지 저장 디렉토리
│   │  └── screenshot/        - 추출 이미지 저장 디렉토리
│   │ 
│   └── templates/            - api + ai 등 기능적 파일 디렉토리
│      ├── ffmpeg.js          - 동영상 처리(이미지 추출) 파일
│      └── kakao_api.py       - kakao vision api
│ 
├── migrations/               - 디비 연동 디렉토리
│
├── node_modules/             - module 디렉토리
│   │ 
├── public/                   - 리액트 디폴드 디렉토리
│   │ 
├── src/                      
│   └── components/           - rendering 할 제작 컴포넌트 디렉토리
│   │  ├── Home.js            - home 화면, 입력 파일과 url 처리
│   │  └── Result.js          - result 화면
│   │
│   └── images/               - static 이미지 디렉토리 (ex. logo)
│
└── App.js                    - components들을 넣을 상위 컴포넌트
```  
