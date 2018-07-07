from flasktasks import db
from enum import Enum
from time import strftime

class Template:
    BASIC = [("To Do", 1, []), ("Doing", 11, []), ("Done", 2, [])]

class Icon(Enum):
    FIRE = 1
    SEND = 2
    SUNGLASSES = 3
    LEAF = 4
    PLANE = 5
    SHOPPING_CART = 6
    GLOBE = 7
    HEART = 8
    USD = 9
    PHONE = 10
    FLASH = 11
    TREE_DECIDUOUS = 12
    KNIGHT = 13
    PIGGY_BANK = 14
    APPLE = 15
    EDUCATION = 16
    ICE_LOLLY_TASTED = 17

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

    def get_num_lists(self):
        return len(List.query.filter(List.board_id == self.board_id).all())

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

    def set_template(self, template):
        if template == 1:
            TEMPLATE = Template.BASIC
        else:
            return

        for idx, (name, icon, tasks) in enumerate(TEMPLATE):
            new_list = List(name, icon, self.id, idx)
            self.lists.append(new_list)

class LogEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(30))
    message = db.Column(db.String(140))

    def __init__(self, message):
        self.message = message
        self.timestamp = strftime("%d-%m-%Y %H:%M:%S")
