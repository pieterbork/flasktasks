# FlaskTasks

A simple Kanban board made with Flask


## Dependencies

**Make sure to use a `python3` environment.**

Install the Following dependencies.

`pip install -e .`

## Running

Before running, you must create the database. Run the `setup_db.py` script to create an initial database and some sample data.
```
python setup_db.py
```

Socket.io provides a web ready interface when eventlet is installed
```
export FLASK_APP=flasktasks
flask run
```

And finally browse to http://localhost:5000

