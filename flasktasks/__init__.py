from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

app = Flask(__name__)
app.secret_key = b'5#y2L"F4Q8z\n\xec]'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flasktasks.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)

import flasktasks.views
import flasktasks.filters
import flasktasks.models
import flasktasks.logger

if __name__ == '__main__':
    socketio.run(app)
