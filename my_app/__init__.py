import os
from my_app import db
from my_app import bp_fornecedores
from flask import Flask, render_template


def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    
    if test_config is None:
        app.config.from_pyfile('config.py', silent = True)
    else:
        app.config.from_mapping(test_config)


    #Garantindo que instance folder exista.

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass



    @app.route('/')
    def hello():
        return render_template('index.html')
    
     
    db.init_app(app)
    app.register_blueprint(bp_fornecedores.bp, url_prefix = '/siga')
    print("Blueprint 'auth' registrado com sucesso!")



    return app


