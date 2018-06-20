from flask import Markup
from flasktasks import app
from flasktasks.plugins import dispatch

@app.template_filter('html_dispatch')
def html_dispatch(board, function):
	values = dispatch(function, board)
	return Markup(''.join(values))
