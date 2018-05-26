from collections import defaultdict, OrderedDict
from flask import Blueprint, Flask, jsonify, render_template, request, session
from os.path import abspath, dirname
import sys

sys.dont_write_bytecode = True
path_app = dirname(abspath(__file__))
if path_app not in sys.path:
    sys.path.append(path_app)

from database import db, create_database
from models import *

hyperOSPF = Blueprint('hyperOSPF_app', __name__)


def allowed_file(name, allowed_extensions):
    allowed_syntax = '.' in name
    allowed_extension = name.rsplit('.', 1)[1].lower() in allowed_extensions
    return allowed_syntax and allowed_extension


@hyperOSPF.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


def configure_database(app):
    create_database()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()
    db.init_app(app)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'key'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.register_blueprint(hyperOSPF)
    configure_database(app)
    return app, generator


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
