## Reference Site

[https://dev.to/divyajyotiuk/how-to-create-react-app-with-flask-backend-2nf7](https://dev.to/divyajyotiuk/how-to-create-react-app-with-flask-backend-2nf7)
without virtual environment setting

## React + Flask

This folder structure is default for React (except : flask_server)
./package.json - proxy (5000)

## Directory
```bash
├── README.md                 - 리드미 파일
│
├── flask_server/             - 백엔드 플라스크 디렉토리
│   ├── app.py                - 서버 시작, 서버 api reply 처리
│   ├── .env                  - 환경 설정 파일
│   │
│   ├── data/                 - 백엔드 image 저장 디렉토리
│   │ 
│   └── templates/            - api + ai 등 기능적 파일 디렉토리
│      └── kakao_api.py       - kakao vision api
│ 
├── node_modules/             - module 디렉토리
│   │ 
├── public/                   - 리액트 디폴드 디렉토리
│   │ 
├── src/                      - 우리가 만질 디렉토리
│   └── components/           - rendering 할 제작 컴포넌트 디렉토리
│   │  ├── Home.js            - home 화면, 입력 파일과 url 처리
│   │  └── Result.js          - result 화면
│   │
│   └── images/               - static 이미지 디렉토리 (ex. logo)
│
└── App.js                    - components들을 넣을 상위 컴포넌트
```

## Steps

in /flask_server  -> flask run  
in ./             -> npm run start  
