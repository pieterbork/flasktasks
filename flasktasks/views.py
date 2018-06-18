from flask import render_template, request, redirect, url_for, abort, jsonify, flash
from collections import defaultdict
from flasktasks import app, db
from flasktasks.models import Board, List, Task, Status, Color, Icon, LogEntry
from flasktasks.signals import task_created, board_created 
import sqlite3

@app.route('/')
def index():
    return redirect(url_for('boards'))
    
@app.route('/future')
def future():
    return render_template('future.html')

@app.route('/boards')
def boards():
    boards = Board.query.all()
    return render_template('boards.html', boards=boards, colors=Color.all_reverse())

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
        return render_template('board/new.html', colors=Color.all())

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

        return render_template('board/index.html', board=board, colors=Color.all_reverse(), icons=Icon.all_reverse())

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
        return render_template('task/new.html', colors=Color.all())

@app.route('/tasks/<int:task_id>', methods=['DELETE', 'GET'])
def task(task_id):
    if request.method == 'DELETE':
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return url_for('board', board_id=task.board_id)
    else:
        task = Task.query.get_or_404(task_id)
        lists = List.query.filter(List.id == task.list_id).all()
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
        return render_template('task/edit.html', task=task, colors=Color.all())

@app.route('/tasks/<int:task_id>/set_status/<status>')
def set_status(task_id, status):
    task = Task.query.get_or_404(task_id)
    board = Board.query.get_or_404(task.board_id)
    current_tasks = board.get_tasks_by_status()
    
    current_list_tasks = current_tasks[Status(task.status).name]
    current_index = current_list_tasks.index(task)
    tasks_need_reorder = current_list_tasks[current_index+1:]
    for t in tasks_need_reorder:
        t.order -= 1
        db.session.add(t)

    order = len(current_tasks[status.upper()])
    try:
        task.status = Status[status.upper()].value
    except KeyError:
        abort(400)
    task.order = order

    db.session.add(task)
    db.session.commit()
    return redirect(url_for('board', board_id=task.board_id))

@app.route('/tasks/<int:task_id>/set_order/<int:order>')
def set_order(task_id, order):
    task = Task.query.get_or_404(task_id)
    board = Board.query.get_or_404(task.board_id)
    current_tasks = board.get_tasks_by_status(task.status)
    current_index = current_tasks.index(task)

    if order > task.order:
        reordered_task = current_tasks[current_index+1]
        reordered_task.order -= 1
    else:
        reordered_task = current_tasks[current_index-1]
        reordered_task.order += 1

    task.order = order
    
    db.session.add(reordered_task)
    db.session.add(task)
    db.session.commit()
    
    return render_template('list')

    
#@app.route('/tasks/<int:task_id>', methods=['DELETE'])
#def delete_task(task_id):
#    task = Task.query.get_or_404(task_id)
#    db.session.delete(task)
#    db.session.commit()
#    return url_for('board', board_id=task.board_id)
    
#@app.route('/boards/<int:board_id>', methods=['DELETE'])
#def delete_board(board_id):
#    board = Board.query.get_or_404(board_id)
#    db.session.delete(board)
#    db.session.commit()
#    return url_for('boards')

#@app.route('/tags/new', methods=['POST', 'GET'])
#def new_tag():
#   if request.method == 'POST':
#       try:
#           color = Color(int(request.form.get('color_id')))
#       except ValueError:
#           abort(400)
#       tag = Tag(request.form.get('name'), color)
#       db.session.add(tag)
#       db.session.commit()
#       return redirect(url_for('boards'))
#   else:
#       colors = { color.name: color.value for color in Color }
#       return render_template('tags/new.html', colors=colors)


@app.route('/log')
def log():
    log_entries = LogEntry.query.all()
    return render_template('log.html', log_entries=log_entries)
