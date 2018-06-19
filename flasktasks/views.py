from flask import render_template, request, redirect, url_for, abort, jsonify, flash
from collections import defaultdict
from flasktasks import app, db
from flasktasks.models import Board, List, Task, Color, Icon, LogEntry
from flasktasks.signals import task_created, board_created 
import sqlite3

@app.context_processor
def inject_template_globals():
    return {
            'colors': Color.all(),
            'colors_rev': Color.all_reverse(),
            'icons': Icon.all(),
            'icons_rev': Icon.all_reverse(),
        }

@app.route('/')
def index():
    return redirect(url_for('boards'))
    
@app.route('/future')
def future():
    return render_template('future.html')

@app.route('/boards')
def boards():
    boards = Board.query.all()
    return render_template('boards.html', boards=boards)

@app.route('/boards/new', methods=['POST', 'GET'])
def new_board():
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('description')
        try:
            color = Color(int(request.form.get('color'))).value
        except:
            color = 1
        board = Board.query.filter(Board.title==title).first()
        if not board:
            board = Board(title, desc, color)
            db.session.add(board)
            db.session.commit()
            board_created.send(board)
            flash('Board was created successfully!')
        else:
            flash('A board with that title already exists!')
            print("Board named {} must already exist".format(title))
        return redirect(url_for('boards'))
    else:
        return render_template('board/new.html')

@app.route('/board/<int:board_id>', methods=['GET', 'DELETE'])
def board(board_id):
    if request.method == 'DELETE':
        board = Board.query.get_or_404(board_id)
        db.session.delete(board)
        db.session.commit()
        return url_for('boards')
    else:
        board = Board.query.get_or_404(board_id)
        tasks_by_status = board.get_tasks_by_status()

        return render_template('board/index.html', board=board)

@app.route('/board/<int:board_id>/lists/new', methods=['POST', 'GET'])
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
        return redirect(url_for('board', board_id=board_id))
    else:
        return render_template('list/new.html', icons=Icon.all())

@app.route('/list/<int:list_id>', methods=['DELETE'])
def delete_list(list_id):
    list = List.query.get_or_404(list_id)

    db.session.delete(list)
    db.session.commit()

    board = Board.query.get_or_404(list.board_id)

    return render_template('list/list_container.html', board=board)


@app.route('/list/<int:list_id>/tasks/new', methods=['POST', 'GET'])
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
        task_created.send(task)
        return redirect(url_for('board', board_id=list.board_id))
    else:
        return render_template('task/new.html')


@app.route('/tasks/<int:task_id>', methods=['DELETE', 'GET'])
def task(task_id):
    if request.method == 'DELETE':
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return url_for('board', board_id=task.board_id)
    else:
        task = Task.query.get_or_404(task_id)
        lists = List.query.filter(List.board_id == task.board_id).all()
        return render_template('task/index.html', lists=lists, task=task, icons=Icon.all_reverse())
    
@app.route('/tasks/<int:task_id>/edit', methods=['POST','GET'])
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
        return redirect(url_for('board', board_id=task.board_id))
    else:
        task = Task.query.get_or_404(task_id)
        return render_template('task/edit.html', task=task)

@app.route('/tasks/<int:task_id>/set_list/<int:list_id>/order/<int:order>', methods=['GET'])
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

    return "Great!"

@app.route('/log')
def log():
    log_entries = LogEntry.query.all()
    return render_template('log.html', log_entries=log_entries)
