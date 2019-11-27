import os

basedir = os.path.abspath(os.path.dirname(__name__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY = ''') or 'ndakdnakdnenekjdnkejdn'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.goooglemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in\
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <mbaamutendwa@gmail.com>'
    FLASK_ADMIN = os.environ.get('FLASK_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    Debug = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'dev_data.db')


class TestingConfig(Config):
    Debug = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'test_data.db')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'prod_data.db')


config = {
    'development': DevelopmentConfig,  # Development configs
    'testing': TestingConfig,  # Testing configs
    'production': ProductionConfig,  # Production configs

    'default': DevelopmentConfig  # Default(Development) configs
}
