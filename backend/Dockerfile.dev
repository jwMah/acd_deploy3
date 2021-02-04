FROM python:3

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update -y
RUN apt-get install -y ffmpeg 
COPY requirements.txt /usr/src/app
RUN pip install -r requirements.txt

CMD ["gunicorn","app:app","-b","0.0.0.0:5000", "-w 3","-k gevent"]
