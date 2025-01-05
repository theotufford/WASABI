import functools
from datetime import date
import json
from flask import (
    Blueprint, flash, g, redirect, current_app, render_template, request, session, url_for
)

from WasabiMain.db import (get_db,wellPos, pumpUpdate)


bp = Blueprint('programmer', __name__, url_prefix='/program')

@bp.route('/', methods=("GET","POST"))
def programmer():
    db = get_db()
    if  request.method == "POST":
        compare_and_update(request.get_json())
        return "meowwww"
        flash(error)
    with current_app.open_resource('./static/resources/config.json') as f:
        PlateInfo = json.loads(f.read())["machineInfo"]["plates"]

    DBplates = json.loads(db.execute('SELECT plateData FROM plateatlas').fetchone()[0])

    PumpContents = json.loads(db.execute('SELECT pumpData FROM pumpatlas').fetchone()[0])

    experiments = db.execute("SELECT title FROM experiments ").fetchall()

    return render_template("programmer/programmer.htm", plates = PlateInfo, DBplates = DBplates, PumpContents = PumpContents, experiments = experiments) 

@bp.route('/test', methods=("GET","POST"))
def test():
    return render_template("programmer/test.htm")


def compare_and_update(package):
    name = package['name']
    data = json.dumps(package['instructions'])
    db = get_db()
    try:
        current = db.execute(
            "SELECT instructions FROM experiments WHERE title = ?", (name,)
        ).fetchone()[0]
    except Exception as e:
        current = None
        pass

    if current is None:
        db.execute(
            "INSERT INTO experiments (title, instructions) VALUES (?, ?)", (name, data,)
        ).fetchall()
        db.commit()

    elif current == data:
        print("duplicate stopped")
    else:
        version = db.execute(
            "SELECT version FROM experiments WHERE title = ?", (name,)
        ).fetchone()[0]
        pastData = f"(version{version}, {current})"
        version = version + 1
        try:
            history = db.execute(
                "SELECT pastRunInstructions FROM experiments WHERE title = ?", (name,)
            ).fetchone()[0]
            history = history + "," + pastData
        except Exception as e:
            history = pastData
        pushtobackup = db.execute(
            "INSERT INTO experiments (pastRunInstructions , version, instructions) VALUES (?,?,?)", (history,version,data,)
        ).fetchall()
        db.commit()



