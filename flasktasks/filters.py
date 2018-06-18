from flask import request
from flasktasks import app

@app.template_filter('is_selected')
def is_board_selected(board_id):
	if str(board_id) == request.args.get('board_id'):
		return "selected"
	else:
		return ''

@app.template_filter('is_current_page')
def is_current_page(current_path):
	if current_path == request.path:
		return "active"
	else:
		return ''

@app.template_filter('human')
def str_to_title(str_val):
	return str_val.title()
