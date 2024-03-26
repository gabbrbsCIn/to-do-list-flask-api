import os
from flask import Flask
from config.initializers import init_app

app = Flask(__name__)
app.config.from_pyfile('config/config.py')

app_user = init_app(app)
db = app_user[0]
ma = app_user[1]
migrate = app_user[2]
bcrypt = app_user[3]
login_manager = app_user[4]


from routes.todolist import *
from routes.users import *
from routes.tasks import *

if __name__ == '__main__':
    app.run(debug=True)
