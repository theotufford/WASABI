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
        experimentInstructions = request.get_json()['instructions']
        experimentTitle = request.get_json()['name'] 
        print(experimentTitle)
        db.execute(
            "INSERT INTO experiments (title, instructions) VALUES (?, ?)", (json.dumps(experimentTitle), json.dumps(experimentInstructions))
        ).fetchall()
        db.commit()
        return experimentInstructions
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
