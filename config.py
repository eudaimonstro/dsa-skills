class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MEMBER_FILE_NAME = 'members.csv'


class ProductionConfig(Config):
    ENV = 'production'
    DEVELOPMENT = False
    DEBUG = False


class DevelopmentConfig(Config):
    ENV = 'development'
    DEVELOPMENT = True
    DEBUG = True
    SERVER_NAME = 'localhost:5000'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development_database.db'
    SQLALCHEMY_ECHO = True
