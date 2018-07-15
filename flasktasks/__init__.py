from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_login import LoginManager
from flasktasks import config

app = Flask(__name__)
app.secret_key = b'5#y2L"F4Q8z\n\xec]'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flasktasks.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"

if not config.LOGIN:
    login_manager.anonymous_user.is_authenticated = True

import flasktasks.views
import flasktasks.filters
import flasktasks.models
import flasktasks.logger

if __name__ == '__main__':
    socketio.run(app)
