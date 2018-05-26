from os import remove
from os.path import abspath, dirname, join, pardir
from pytest import fixture
import sys

path_test = dirname(abspath(__file__))
path_parent = abspath(join(path_test, pardir))
path_examples = join(path_parent, 'examples')
path_app = join(path_parent, 'swap')
if path_app not in sys.path:
    sys.path.append(path_app)

from flask_app import create_app


@fixture
def client():
    app, solver = create_app()
    client = app.test_client()
    with app.app_context():
        yield client
    remove(join(path_test, 'database.db'))
