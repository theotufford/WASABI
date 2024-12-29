import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'WasabiData.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # import the database into the app
    from . import db
    db.init_app(app)

    from . import home 
    app.register_blueprint(home.bp)

    from . import programmer
    app.register_blueprint(programmer.bp)

    from . import agent
    app.register_blueprint(agent.bp)

    from . import middleMan
    app.register_blueprint(middleMan.bp)

    return app
