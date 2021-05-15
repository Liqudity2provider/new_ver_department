import nose2
from flask_testing import TestCase

from app import db
from config import app_config
from run import app

app.config.from_object(app_config['test'])


class TestBase(TestCase):

    def create_app(self):
        return app

    def setUp(self) -> None:
        self.app = app.test_client()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    nose2.run()