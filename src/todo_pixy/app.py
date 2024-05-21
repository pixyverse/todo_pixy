from flask import Flask, request
from todo_pixy.templates import index
from todo_pixy.templates.add_todo import (
    add_todo_success_repsonse,
)

app = Flask(__name__, static_url_path="", static_folder="static")


@app.route("/addTODO", methods=["POST"])
def add_todo():
    input_new_todo = request.form.get("new-todo")
    if input_new_todo and input_new_todo.strip() != "":
        return add_todo_success_repsonse(input_new_todo.strip())
    return "Not a valid todo", 400


@app.route("/")
def hello_world():
    return index.doc
