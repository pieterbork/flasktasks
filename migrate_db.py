import sqlite3
from flasktasks import db
from flasktasks.config import DB_PATH

with sqlite3.connect(DB_PATH) as con:
    c = con.cursor()

    c.execute("ALTER TABLE boards RENAME TO old_boards")
    c.execute("ALTER TABLE lists RENAME TO old_lists")
    c.execute("ALTER TABLE tasks RENAME TO old_tasks")

    db.create_all()

    c.execute("""SELECT id, title, description, color
                 FROM old_boards
                 ORDER BY id ASC""")

    boards = [(row[0], row[1], row[2], row[3]) for row in c.fetchall()]
    c.executemany("""INSERT INTO boards (id, title, description, color)
                 VALUES (?, ?, ?, ?)""", boards)

    c.execute("""SELECT id, title, icon, color, [order], board_id
                 FROM old_lists
                 ORDER by id ASC""")

    lists = [(row[0], row[1], row[2], row[3], row[4], row[5]) for row in c.fetchall()]
    c.executemany("""INSERT INTO lists (id, title, icon, color, [order], board_id)
                 VALUES (?, ?, ?, ?, ?, ?)""", lists)

    c.execute("""SELECT id, title, description, color, [order], board_id, list_id
                 FROM old_tasks
                 ORDER by id ASC""")

    tasks = [(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in c.fetchall()]
    c.executemany("""INSERT INTO tasks (id, title, description, color, [order], board_id, list_id)
                 VALUES (?, ?, ?, ?, ?, ?, ?)""", tasks)
