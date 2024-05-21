from http.client import OK
from flask import Flask
from todo_pixy.templates import index

app = Flask(__name__, static_url_path="", static_folder="static")


@app.route("/")
def hello_world():
    return index.doc
