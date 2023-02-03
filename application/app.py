from flask import Flask
from flask_mongoengine import MongoEngine
from config import BaseConfig


def init_app(config_obj=BaseConfig):
    flask_app = Flask(__name__, static_url_path='/static')
    flask_app.config.from_object(config_obj)
    db = configure_extensions(flask_app)

    from application.views.user_list import user_list_bp
    flask_app.register_blueprint(user_list_bp)
    return flask_app, db


def configure_extensions(app):
    return MongoEngine(app)


# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'
#
#
#
# if __name__ == '__main__':
#     app.run()
