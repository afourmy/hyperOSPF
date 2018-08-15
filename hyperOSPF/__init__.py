from collections import defaultdict, OrderedDict
from flask import Blueprint, Flask, jsonify, render_template, request
from .graph_generator import GraphGenerator

hyperOSPF = Blueprint('hyperOSPF', __name__)
generator = GraphGenerator()

@hyperOSPF.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', buttons=generator.algorithms)


@hyperOSPF.route('/generate/<algorithm>/<dimension>', methods=['POST'])
def generate_graph(algorithm, dimension):
    return jsonify(getattr(generator, algorithm)(int(dimension)))


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'key'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.register_blueprint(hyperOSPF)
    return app
