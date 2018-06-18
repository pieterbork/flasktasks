from flasktasks import app, db
from flasktasks.models import LogEntry
from flasktasks.signals import task_created, board_created 

@task_created.connect
def log_task_creation(task, **kwargs):
	message = "The task \"%s\" was created." % task.title
	log_entry(message)

@board_created.connect
def log_board_creation(board, **kwargs):
	message = "The board \"%s\" was created." % board.title
	log_entry(message)

def log_entry(message):
	log_entry = LogEntry(message)
	db.session.add(log_entry)
	db.session.commit()
