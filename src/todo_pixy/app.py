from flask import Flask, request
from sqlalchemy import delete, func, select, update
from todo_pixy.model import TODO, TODOSTATUS, Base
from todo_pixy.templates import index
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(model_class=Base)

app = Flask(__name__, static_url_path="", static_folder="static")
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
# initialize the app with the extension
db.init_app(app)
with app.app_context():
    db.create_all()


def get_active_todo_count():
    stmt = (
        select(func.count("*")).select_from(TODO).where(TODO.status == TODOSTATUS.todo)
    )
    result = db.session.scalars(stmt).one()
    return index.todo_counter("todo_counter", {"count": result, "oob": True})


@app.route("/todo/<int:todo_id>", methods=["GET"])
def get_todo(todo_id: int):
    stmt = select(TODO).where(TODO.id == todo_id)
    todo_row = db.session.execute(stmt).one()
    if todo_row:
        return index.todo_item("todo_item", {"todo": todo_row.TODO}, [])
    return "Not found", 404


@app.route("/addTODO", methods=["POST"])
def add_todo():
    input_new_todo = request.form.get("new-todo")
    if input_new_todo and input_new_todo.strip() != "":
        new_todo = TODO(todo=input_new_todo.strip(), status=TODOSTATUS.todo)
        db.session.add(new_todo)
        db.session.commit()
        return (
            index.todo_item("todo_item", {"todo": new_todo}, [])
            + get_active_todo_count()
        )
    return "Not a valid todo", 400


@app.route("/updateTodo/<int:todo_id>", methods=["POST"])
def update_todo(todo_id: int):
    updated_todo = request.form.get("edit-todo")
    trimmed_update = updated_todo.strip()
    if updated_todo and trimmed_update:
        stmt = update(TODO).where(TODO.id == todo_id).values(todo=updated_todo.strip())
        db.session.execute(stmt)
        db.session.commit()
        stmt = select(TODO).where(TODO.id == todo_id)
        todo_row = db.session.execute(stmt).one()
        return index.todo_item("todo_item", {"todo": todo_row.TODO}, [])
    else:
        stmt = delete(TODO).where(TODO.id == todo_id)
        db.session.execute(stmt)
        db.session.commit()
        return get_active_todo_count(), 200


@app.route("/todo/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id: int):
    stmt = delete(TODO).where(TODO.id == todo_id)
    db.session.execute(stmt)
    db.session.commit()
    return get_active_todo_count(), 200


@app.route("/toggle/<int:todo_id>", methods=["POST"])
def toggle(todo_id: int):
    stmt = select(TODO).where(TODO.id == todo_id)
    todo_row = db.session.execute(stmt).one()
    if todo_row:
        if todo_row.TODO.status == TODOSTATUS.completed:
            todo_row.TODO.status = TODOSTATUS.todo
        else:
            todo_row.TODO.status = TODOSTATUS.completed
        db.session.commit()
        return (
            index.todo_item("todo_item", {"todo": todo_row.TODO}, [])
            + get_active_todo_count()
        )
    return "Unable to toggle", 400


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
    return (
        index.todo_list(
            "todo_list", {"todos": db.session.scalars(select(TODO)).all()}, []
        )
        + get_active_todo_count()
    )


@app.route("/clearCompleted", methods=["POST"])
def clear_completed():
    stmt = delete(TODO).where(TODO.status == TODOSTATUS.completed)
    db.session.execute(stmt)
    db.session.commit()
    return (
        index.todo_list(
            "todo_list", {"todos": db.session.scalars(select(TODO)).all()}, []
        )
        + get_active_todo_count()
    )


@app.route("/all")
def all():
    return (
        index.todo_list(
            "todo_list",
            {"todos": db.session.scalars(select(TODO)).all()},
            [],
        )
        + get_active_todo_count()
    )


@app.route("/active")
def active():
    return (
        index.todo_list(
            "todo_list",
            {
                "todos": db.session.scalars(
                    select(TODO).where(TODO.status == TODOSTATUS.todo)
                ).all()
            },
            [],
        )
        + get_active_todo_count()
    )


@app.route("/completed")
def completed():
    return (
        index.todo_list(
            "todo_list",
            {
                "todos": db.session.scalars(
                    select(TODO).where(TODO.status == TODOSTATUS.completed)
                ).all()
            },
            [],
        )
        + get_active_todo_count()
    )


@app.route("/")
def home():
    all_todo_stmt = select(TODO)
    return index.doc(db.session.scalars(all_todo_stmt).all()) + get_active_todo_count()
