import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, json
)

from WasabiMain.db import get_db

bp = Blueprint('agent', __name__, url_prefix='/agent')

@bp.route('/sessionput', methods=['POST'])
def sessionPut():
    keyForUpdatedValue = request.get_json()["key"]
    updatedValue = request.get_json()["updatedValue"]
    session[keyForUpdatedValue] = updatedValue; 
    for obj in session:
        print(json.dumps(session[obj]))
    return json.dumps({"out":"session updated!", "sessionDump" : session["ExperimentMemory"]})
@bp.route('/sessionget', methods=['POST'])
def sessionGet(): 
    sessionGetResponse = {"out" : "no saved Experiment In session"}
    try:
        keyVal = request.get_json()["key"]
        getVal = session[keyVal]
        sessionGetResponse["out"] = getVal
    except Exception as e:
        print("no data")
    return sessionGetResponse

