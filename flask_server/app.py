from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def say_hello_world():
    return {'result': "Hello World"}