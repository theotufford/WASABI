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


@bp.route('/experiment_to_machinecode', methods=["POST"])
def translator():
    experimentName = request.get_json()["Name"]
    db=get_db()
    print(db.execute('SELECT instructions FROM experiments WHERE title = ?', ("blue",)).fetchone())
    data = json.loads(db.execute('SELECT instructions FROM experiments WHERE title = ?', ("blue",)).fetchone())
    try:
        runcount = json.loads(db.execute(f"SELECT runcount FROM experiments WHERE title = '{experimentName}'").fetchone()[0])
    except:
        runcount = 0

    #generate volume Atlas
    volumeAtlas = {}
    for idx in range(1, len(data)+1):
        instructionform = data[f"instructionform{idx}"]
        for key, value in translate(instructionform):
            try:
                volumeAtlas[key][0]
            except:
                volumeAtlas[key] = []
        volumeAtlas[key].append(value)

    #generate pseudo G code file from volumeAtlas
    #ex:
    #./machineCode/example_run0_experiment_Machine_Code.txt
    #start
    # MW-a1;
    # z-!OffsetDistance;
    # d-stuff-10(ml);
    # d-otherstuff-20(ml);
    # z-OffsetDistance;
    # MW-a2;
    # z-OffsetDistance;
    # d-morestuff-5
    # d-evenMoreStuff-15;
    # z-OffsetDistance;
    # end

    with open(f"./machineCode/{experimentName}_run{runcount}_experiment_Machine_Code.txt", 'w') as mc:
        mc.write("start")
        for key, value in volumeAtlas:
            mc.write(f"MW-{key};\nZ-!OffsetDistance;\n")
            for pair in value:
                mc.write(f"D-{pair['contents']}-{pair['volume']};\n")
            mc.write("z-OffsetDistance;\n")
        mc.write("end")


#method Translator code because idk how to make this import from a different file correctly and honestly I dont care enough to figure it out 
def rowDist(wella, wellb):
    row_a = ord(wella[0].lower()) - ord('a')  
    row_b = ord(wellb[0].lower()) - ord('a')  

    return abs(row_a-row_b)

def columnDist(wella, wellb):
    column_a = int(wella[1:])
    column_b = int(wellb[1:])
    return abs(column_a - column_b)

def gradient(info):
    wells = info["wellids"]
    direction = info["methodInfo"]["direction"]
    contents = info["contents"]
    increment = info["methodInfo"]["increment"]
    intital_volume = info["methodInfo"]["intitalVolume"]
    volumeMap = {}

    match direction:
        case "right":
            for well in wells:
                volume = columnDist(wells[0], well) * increment + intital_volume # distance between initial and final columns * increment + intitial 
                volumeMap[well] = {contents:contents, volume:volume} 
        case "down":
            for well in wells:
                volume = rowDist(wells[0], well) * increment + intital_volume # distance between initial and final row * increment + initial 
                volumeMap[well] = {contents:contents, volume:volume} 
        case "left":
            for well in wells:
                volume = columnDist(wells[-1], well) * increment + intital_volume
                volumeMap[well] = {contents:contents, volume:volume} 
        case"up":
            for well in wells:
                volume = rowDist(wells[-1], well) * increment + intital_volume
                volumeMap[well] = {contents:contents, volume:volume}
    return volumeMap

def constant_volume(info):
    contents = info["contents"]
    wells = info["wells"]
    volume = info['methodInfo']["volume"]
    volumeMap = dict.fromkeys(wells, {contents:contents, volume:volume} )
    return volumeMap


def translate(info):
    method = info["method"]
    match method:
        case "gradient":
            return gradient(info)
        case "constantVolume":
            return constant_volume(info)

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

