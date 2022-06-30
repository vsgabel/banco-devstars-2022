import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SSL_REDIRECT = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

    @staticmethod
    def init_app(app):
        import logging
        from logging import FileHandler

        handler = FileHandler("log.log", "a")
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)

class HerokuConfig(ProductionConfig):
    SSL_REDIRECT = True if os.getenv('DYNO') else False

    @staticmethod
    def init_app(app):
        import logging
        from logging import FileHandler

        handler = FileHandler("log.log", "a")
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)

        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}