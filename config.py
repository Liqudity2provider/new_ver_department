import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """Configuration"""

    SECRET_KEY = os.urandom(32)
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///new_db.db'


class DevelopmentConfig(Config):
    """Development config"""

    DEBUG = True


class ProductionConfig(Config):
    """Production config"""

    DEBUG = False
    TESTING = False


class TestConfig(Config):
    """Testing config"""

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///new_db.db'
    PRESERVE_CONTEXT_ON_EXCEPTION = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestConfig
}
