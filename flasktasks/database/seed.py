from flasktasks import db
from flasktasks.models import Tag, Board, Task, Color


def create_tags():
	tag1 = Tag("Work", Color.BLUE)
	tag2 = Tag("College", Color.RED)
	tag3 = Tag("Side Project", Color.GREEN)
	
	db.session.add(tag1)
	db.session.add(tag2)
	db.session.add(tag3)
	db.session.commit()

def create_boards():
	board1 = Board("Finish Stuff", 'Just finish some stuff', 1)
	board2 = Board("Whatever Class", 'Accomplish that impossible goal', 2)
	board3 = Board("Second Release", 'Pretend to be productive', 3)

	db.session.add(board1)
	db.session.add(board2)
	db.session.add(board3)
	db.session.commit()

def create_tasks():
	for i in range(1, 4):
		task1 = Task("First Task", "Some useful description", i)
		task2 = Task("Second Task", "Some useful description", i)
		task3 = Task("Third Task", "Some useful description", i)

		db.session.add(task1)
		db.session.add(task2)
		db.session.add(task3)
	db.session.commit()

def run_seed():
	print("Creating Tags...")
	create_tags()

	print("Creating Boards...")
	create_boards()

	print("Creating Tasks...")
	create_tasks()
