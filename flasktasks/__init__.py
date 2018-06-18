from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = b'5#y2L"F4Q8z\n\xec]'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flasktasks.db'
db = SQLAlchemy(app)

import flasktasks.views
import flasktasks.filters
import flasktasks.plugin_filters
import flasktasks.models
import flasktasks.logger

from flasktasks.plugins import load_plugins

load_plugins()
