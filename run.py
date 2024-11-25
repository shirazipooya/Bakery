import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from app import app, socketio

if __name__ == '__main__':
    socketio.run(
        app=app,
        host="127.0.0.1",
        port=5000
    )
