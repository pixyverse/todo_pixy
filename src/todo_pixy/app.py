from typing import List
from flask import Flask, request
from sqlalchemy import select, update
from todo_pixy.model import TODO, TODOSTATUS, Base
from todo_pixy.templates import index
from todo_pixy.templates.add_todo import (
    add_todo_success_repsonse,
)
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(model_class=Base)

app = Flask(__name__, static_url_path="", static_folder="static")
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
# initialize the app with the extension
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/addTODO", methods=["POST"])
def add_todo():
    input_new_todo = request.form.get("new-todo")
    if input_new_todo and input_new_todo.strip() != "":
        db.session.add(TODO(todo=input_new_todo.strip(), status=TODOSTATUS.todo))
        db.session.commit()
        return add_todo_success_repsonse(input_new_todo.strip())
    return "Not a valid todo", 400


@app.route("/toggleAll", methods=["POST"])
def toggle_all():
    print("Toggle All TODOS")
    isToggled = request.form.get("toggle-all")
    if isToggled:
        stmt = update(TODO).values(status=TODOSTATUS.completed)
        db.session.execute(stmt)
    else:
        stmt = update(TODO).values(status=TODOSTATUS.todo)
        db.session.execute(stmt)
    db.session.commit()
    return index.todo_list("todo_list", {"todos": db.session.scalars(select(TODO))}, [])


@app.route("/")
def home():
    all_todo_stmt = select(TODO)
    return index.doc(db.session.scalars(all_todo_stmt))
