import os
import tempfile
import app
import pytest


@pytest.fixture
def client():
    db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
    app.app.config['test'] = True

    with app.app.test_client() as client:
        with app.app.app_context():
            app.db.init_db(app.app)
            # app.db.create_all(app=app)
        yield client

    os.close(db_fd)
    os.unlink(app.app.config['DATABASE'])


def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No entries here so far' in rv.data
