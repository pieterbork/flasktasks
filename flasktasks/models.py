from flasktasks import db
from enum import Enum
from time import strftime


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

class Template:
    BASIC = [
        ("To Do", Icon.FIRE.value, []), 
        ("Doing", Icon.FLASH.value, []), 
        ("Done", Icon.SEND.value, [])
    ]

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

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    name = db.Column(db.String(70))

    def __init__(self, username, name):
        self.username = username
        self.name = name

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    description = db.Column(db.String(140))
    color = db.Column(db.Integer)
    order = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'))

    def __init__(self, title, description, list_id, board_id, order, color=Color.GRAY.value):
        self.title = title
        self.description = description
        self.color = color
        self.order = order
        self.list_id = list_id
        self.board_id = board_id

    def __repr__(self):
        return "<Task(id='{}', title='{}', description='{}', color='{}', order='{}', list_id='{}', board_id='{}')>".format(self.id, self.title, self.description, self.color, self.order, self.list_id, self.board_id)

class List(db.Model):
    __tablename__ = "lists"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    icon = db.Column(db.Integer)
    color = db.Column(db.Integer)
    order = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))
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

    def __repr__(self):
        return "<List(id='{}', title='{}', icon='{}', color='{}', order='{}', board_id='{}')>".format(self.id, self.title, self.icon, self.color, self.order, self.board_id)

class Board(db.Model):
    __tablename__ = "boards"
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

    def __repr__(self):
        return "<Board(id='{}', title='{}', description='{}', color='{}')>".format(self.id, self.title, self.description, self.color)

class LogEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(140))
    timestamp = db.Column(db.String(30))

    def __init__(self, message, timestamp=strftime("%d-%m-%Y %H:%M:%S")):
        self.message = message
        self.timestamp = timestamp

    def __repr__(self):
        return "<LogEntry(id='{}', message='{}', timestamp='{}')>".format(self.id, self.message, self.timestamp)
