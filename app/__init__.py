"""
Init departments app
SQLAlchemy config
"""
import logging
from logging import FileHandler, Formatter
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate


from config import app_config

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


def create_app(config_name):
    """Flask application factory"""
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    @app.errorhandler(404)
    def error404(error):
        """Render error page for 400 error"""
        return render_template('error404.html', error=error), 404

    @app.errorhandler(500)
    def error500(error):
        """Render error page for 500 error"""
        return render_template('error500.html', error=error), 500

    return app


app = create_app('development')
api = Api(app=app)


file_handler = FileHandler('error.log')
file_handler.setFormatter(
    Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
)
app.logger.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
