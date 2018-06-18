from blinker import Namespace

flasktasks_signals = Namespace()
task_created = flasktasks_signals.signal('task-created')
board_created = flasktasks_signals.signal('board-created')
