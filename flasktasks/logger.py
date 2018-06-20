from flasktasks import app, db
from flasktasks.models import LogEntry

#Add socketio listeners to create log messages here

def log_entry(message):
	log_entry = LogEntry(message)
	db.session.add(log_entry)
	db.session.commit()
