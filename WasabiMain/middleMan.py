import functools 
import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from WasabiMain.db import (get_db, pumpUpdate)

bp = Blueprint('middleMan', __name__, url_prefix='/middleMan')

def translateExperiment(inputDict):
   pass 


@bp.route('/translateExperiment', methods = ['POST'])
def runExperiment():
    pass

@bp.route('/DirectRun', methods = ['POST'])
def DirectRun():
    pass
