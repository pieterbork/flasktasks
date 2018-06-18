from flasktasks import db
from enum import Enum
from time import strftime


class Status(Enum):
    TO_DO = 1
    DOING = 2
    DONE = 3

class Icon(Enum):
    FIRE = 1
    SEND = 2
    SUNGLASSES = 3

    def all():
        return {icon.name: icon.value for icon in Icon}
    def all_reverse():
        return {icon.value: icon.name for icon in Icon}

class Color(Enum):
    GRAY = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4
    RED = 5

    def all():
        return {color.name: color.value for color in Color}
    def all_reverse():
        return {color.value: color.name for color in Color}

class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    description = db.Column(db.String(140))
    status = db.Column(db.Integer)
    color = db.Column(db.Integer)
    order = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))

    def __init__(self, title, description, list_id, board_id, order, color=Color.GRAY.value):
        self.title = title
        self.description = description
        self.status = Status.TO_DO.value
        self.board_id = board_id
        self.list_id = list_id
        self.order = order
        self.color = color


class List(db.Model):
    __tablename__ = "list"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    icon = db.Column(db.Integer)
    color = db.Column(db.Integer)
    order = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    tasks = db.relationship('Task', backref='list', lazy='dynamic')

    def __init__(self, title, icon, board_id, order, color=Color.GRAY.value):
        self.title = title
        self.icon = icon
        self.board_id = board_id
        self.order = order
        self.color = color

    def get_tasks(self):
        return list(self.tasks.order_by(Task.order))

class Board(db.Model):
    __tablename__ = "board"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(210))
    color = db.Column(db.Integer)
    tasks = db.relationship('Task', backref='board', lazy='dynamic')
    lists = db.relationship('List', backref='board', lazy='dynamic')

    def __init__(self, title, description, color=Color.GRAY.value):
        self.title = title
        self.description = description
        self.color = color

    def get_lists(self):
        return list(self.lists.order_by(List.order))

    def get_num_tasks(self):
        return len(list(Task.query.filter(Task.board_id == self.id)))

    def get_tasks_by_status(self, status=None):
        if status:
            return list(self.tasks.filter(Task.status==status).order_by(Task.order))
        else:
            return {
                "TO_DO": list(self.tasks.filter(Task.status==Status["TO_DO"].value).order_by(Task.order)),
                "DOING": list(self.tasks.filter(Task.status==Status["DOING"].value).order_by(Task.order)),
                "DONE": list(self.tasks.filter(Task.status==Status["DONE"].value).order_by(Task.order))
                }

#class Tag(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   name = db.Column(db.String(20), unique=True)
#   color = db.Column(db.Integer)
#   boards = db.relationship('Board', backref='tag', lazy='dynamic')
#
#   def __init__(self, name, color=Color.GREY):
#       self.name = name
#       self.color = color.value
#   
#   def style(self):
#       color = Color(self.color)
#       return "tagged tag-%s" % color.name.lower()


class LogEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(30))
    message = db.Column(db.String(140))

    def __init__(self, message):
        self.message = message
        self.timestamp = strftime("%d-%m-%Y %H:%M:%S")
