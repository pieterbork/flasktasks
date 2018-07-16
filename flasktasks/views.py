from flask import render_template, request, redirect, url_for, abort, jsonify, flash, make_response
from collections import defaultdict
from flasktasks import app, db, socketio, login_manager, config
from flasktasks.models import User, Board, List, Task, Color, Icon, LogEntry
from flasktasks.utils import ldap_login
from flask_login import login_required, login_user, logout_user
import sqlite3
import flask_socketio as socket

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.context_processor
def inject_template_globals():
    return {
            'colors': Color.all(),
            'colors_rev': Color.all_reverse(),
            'icons': Icon.all(),
            'icons_rev': Icon.all_reverse(),
        }

@app.route('/')
@login_required
def index():
    return redirect(url_for('boards'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get('user')
        password = request.form.get('password')

        if not username or not password:
            flash("Please supply both username and password.", 'error')
            return redirect('/login')

        ldap_user = ldap_login(username, password)
        if ldap_user:
            user = User.query.filter(User.username==username).first()
            if not user:
                user = User(username, "Test")
                db.session.add(user)
                db.session.commit()
            print("Logging in user")
            login_user(user)
            return redirect('/')
        else:
            flash("Invalid login", 'error')
            print("Bad Login")
            return redirect('/login')
    else:
        return render_template('login.html')

@app.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect('/')
    
@app.route('/future')
def future():
    return render_template('future.html')

@app.route('/boards', methods=['GET'])
@login_required
def boards():
    boards = Board.query.all()
    return render_template('boards.html', boards=boards)

@app.route('/board_container', methods=['GET'])
@login_required
def board_container():
    boards = Board.query.all()
    return render_template('board/board_container.html', boards=boards)

@app.route('/boards/new', methods=['POST', 'GET'])
@login_required
def new_board():
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('description')
        template = int(request.form.get('template'))
        try:
            color = Color(int(request.form.get('color'))).value
        except:
            color = 1
        board = Board.query.filter(Board.title==title).first()
        if not board:
            board = Board(title, desc, color)
            if template:
                board.set_template(template)
            db.session.add(board)
            db.session.commit()
            socketio.emit('board_create', namespace='/boards')
            flash('Board was created successfully!', 'success')
        else:
            flash('A board with that title already exists!', 'error')
            print("Board named {} must already exist".format(title))
        return redirect(url_for('boards'))
    else:
        return render_template('board/new.html')

@app.route('/board/<int:board_id>', methods=['GET', 'DELETE'])
@login_required
def board(board_id):
    if request.method == 'DELETE':
        board = Board.query.get_or_404(board_id)
        db.session.delete(board)
        db.session.commit()
        socketio.emit('board_delete', namespace='/board/{}'.format(board_id))
        socketio.emit('board_delete', namespace='/boards')
        return url_for('boards')
    else:
        board = Board.query.get_or_404(board_id)

        return render_template('board/index.html', board=board)

@app.route('/board/<int:board_id>/edit', methods=['POST','GET'])
@login_required
def edit_board(board_id):
    if request.method == 'POST':
        board = Board.query.get_or_404(board_id)
        board.title = request.form.get('title')
        board.description = request.form.get('description')
        try:
            board.color = Color(int(request.form.get('color'))).value
        except:
            pass
        db.session.commit()
        #@TODO ADD SOCKETIO EMIT
        return redirect(url_for('board', board_id=board_id))
    else:
        board = Board.query.get_or_404(board_id)
        return render_template('board/edit.html', board=board)

@app.route('/board/<int:board_id>/lists/new', methods=['POST', 'GET'])
@login_required
def new_list(board_id):
    if request.method == 'POST':
        board = Board.query.get_or_404(board_id)
        lists = board.get_lists()
        title = request.form.get('title')
        try:
            icon = Icon(int(request.form.get('icon'))).value
        except:
            icon = 1
        order = len(lists)
        li = List(title, icon, board_id, order)
        db.session.add(li)
        db.session.commit()
        socketio.emit('task_update', namespace='/board/{}'.format(board_id))
        return redirect(url_for('board', board_id=board_id))
    else:
        return render_template('list/new.html')

@app.route('/board/<int:board_id>/list_container')
@login_required
def list_container(board_id):
    board = Board.query.get_or_404(board_id)
    return render_template('list/list_container.html', board=board)

@app.route('/list/<int:list_id>', methods=['DELETE'])
@login_required
def delete_list(list_id):
    list = List.query.get_or_404(list_id)

    db.session.delete(list)
    db.session.commit()

    board = Board.query.get_or_404(list.board_id)
    socketio.emit('task_update', namespace='/board/{}'.format(board.id))

    return render_template('list/list_container.html', board=board)

@app.route('/list/<int:list_id>/edit', methods=['POST','GET'])
@login_required
def edit_list(list_id):
    if request.method == 'POST':
        list = List.query.get_or_404(list_id)
        list.title = request.form.get('title')
        try:
            list.icon = Icon(int(request.form.get('icon'))).value
        except:
            list.icon = 1
        db.session.commit()
        socketio.emit('task_update', namespace='/board/{}'.format(list.board_id))
        return redirect(url_for('board', board_id=list.board_id))
    else:
        list = List.query.get_or_404(list_id)
        return render_template('list/edit.html', list=list)

@app.route('/list/<int:list_id>/tasks/new', methods=['POST', 'GET'])
@login_required
def new_task(list_id):
    if request.method == 'POST':
        list = List.query.get_or_404(list_id)
        tasks = list.get_tasks()
        order = len(tasks)
        title = request.form.get('title')
        desc = request.form.get('description')
        try:
            color = Color(int(request.form.get('color'))).value
        except:
            color = 1
        task = Task(title, desc, list_id, list.board_id, order, color)
        db.session.add(task)
        db.session.commit()
        socketio.emit('task_update', namespace='/board/{}'.format(task.board_id))
        return redirect(url_for('board', board_id=list.board_id))
    else:
        return render_template('task/new.html')


@app.route('/tasks/<int:task_id>', methods=['DELETE', 'GET'])
@login_required
def task(task_id):
    if request.method == 'DELETE':
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        socketio.emit('task_update', namespace='/board/{}'.format(task.board_id))
        return url_for('board', board_id=task.board_id)
    else:
        task = Task.query.get_or_404(task_id)
        lists = List.query.filter(List.board_id == task.board_id).all()
        return render_template('task/index.html', lists=lists, task=task)
    
@app.route('/tasks/<int:task_id>/edit', methods=['POST','GET'])
@login_required
def edit_task(task_id):
    if request.method == 'POST':
        task = Task.query.get_or_404(task_id)
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        try:
            task.color = Color(int(request.form.get('color'))).value
        except:
            pass
        db.session.commit()
        socketio.emit('task_update', namespace='/board/{}'.format(task.board_id))
        return redirect(url_for('board', board_id=task.board_id))
    else:
        task = Task.query.get_or_404(task_id)
        return render_template('task/edit.html', task=task)

@app.route('/tasks/<int:task_id>/set_list/<int:list_id>/order/<int:order>', methods=['GET'])
@login_required
def set_order(task_id, list_id, order):
    task = Task.query.get_or_404(task_id)
    current_list = List.query.get_or_404(task.list_id)

    if list_id != task.list_id:
        current_tasks = current_list.get_tasks()
        current_index = current_tasks.index(task)
        current_list.tasks.remove(task)
        for t in current_tasks[current_index+1:]:
            t.order -= 1
        new_list = List.query.get_or_404(list_id)
        new_tasks = new_list.get_tasks()
        task.order = len(new_tasks)
        new_list.tasks.append(task)
        current_list = new_list
        db.session.commit()

    current_tasks = current_list.get_tasks()

    if order < task.order:
        for t in current_tasks[order:task.order]:
            t.order += 1
    elif order > task.order:
        for t in current_tasks[task.order+1:order+1]:
            t.order -= 1

    task.order = order
    db.session.commit()

    socketio.emit('task_update', namespace='/board/{}'.format(task.board_id))

    return "Great!"

@app.route('/log')
@login_required
def log():
    log_entries = LogEntry.query.all()
    return render_template('log.html', log_entries=log_entries)
