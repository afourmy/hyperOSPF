from hyperOSPF import create_app


@fixture
def client():
    app, solver = create_app()
    client = app.test_client()
    with app.app_context():
        yield client

