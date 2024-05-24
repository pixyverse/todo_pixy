# TODO-PIXY
This is an implementation of the infamous todomvc app which has a detailed spec here. While todomvc focuses on client-side scripting to implement all features, todo-pixy focuses on implementing [HATEOAS](https://htmx.org/essays/hateoas/) principles with python using [pixy](https://github.com/pixyverse/pixy) for components.

Minimal client side scripting is handled using the excellent [hyperscript](http://hyperscript.org) package.
# Requirements

* NPM (only to install TODOMVC template dependencies)
* python [poetry](https://python-poetry.org) to install dependencies
## Key dependencies.

* [PixyVerse.Pixy](https://github.com/pixyverse/pixy)
* [PixyVerse.render_HTML](https://github.com/pixyverse/render_html)
* [Flask](https://flask.palletsprojects.com/en/3.0.x/)
* Sqlite/[SQLAlchemy](https://www.sqlalchemy.org) for persistence

## Optional

[fswatch](https://emcrisostomo.github.io/fswatch/) to automatically transpile (.pix) files on change to python modules

# Install and Run

1. Git checkout the project
2. ```poetry install```
3. ```cd src/todo_pixy```
4. ```flask run --debug```
5. In another terminal session run the pixy transpiler on all .pix files, you can use the handy proc.sh script.

    ```
    fswatch src/todo_pixy/templates/**/*.pix | ./proc.sh
    ```
