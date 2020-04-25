from flask import Flask
from flask_sockets import Sockets
import datetime
import time
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

app = Flask(__name__)
sockets = Sockets(app)

@app.route('/')
def index():
    return "Hello"

@sockets.route('/test')
def test(ws):
    while not ws.closed:
        ws.send(1)
        time.sleep(1)

if __name__ == "__main__":
    server = pywsgi.WSGIServer(('0.0.0.0',8088),application=app,handler_class=WebSocketHandler)
    server.serve_forever()
