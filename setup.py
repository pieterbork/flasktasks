from setuptools import setup

setup(
    name='Flasktasks',
    packages=['flasktasks'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'flask_login',
        'flask-socketio',
        'eventlet'
    ]
)
