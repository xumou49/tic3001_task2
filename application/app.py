from datetime import timedelta

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from application.models.login import Login
from application.services.auth import UserPrincipal
from application.services.exceptions import AuthenticationException
from config import BaseConfig


def init_app(config_obj=BaseConfig):
    flask_app = Flask(__name__, static_url_path='/static')
    flask_app.config.from_object(config_obj)
    db = configure_extensions(flask_app)

    from application.views.user_list import user_list_bp
    flask_app.register_blueprint(user_list_bp)

    from application.views.login_auth import login_auth_bp
    flask_app.register_blueprint(login_auth_bp)
    return flask_app, db


def configure_extensions(app):
    CORS(app)
    db = MongoEngine(app)

    # flask JWT configuration
    app.config["JWT_SECRET_KEY"] = app.config['JWT_SECRETS']
    app.config["JWT_ALGORITHM"] = app.config['JWT_ALGORITHM']
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=3)
    jwt = JWTManager(app)

    # flask login
    from flask_login import LoginManager
    login = LoginManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(user_login):
        return user_login.username if isinstance(user_login, Login) else user_login['username']

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        user_id = jwt_data['sub']

        return UserPrincipal(user_id,
                             jwt_data['claims'],
                             jwt_data['is_super_admin'],
                             login)

    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        if not isinstance(identity, Login):
            return {}

        permissions = app.config['VIEWER_CLAIMS']

        user_role = identity.role
        if user_role == Login.Role.ADMIN.value:
            permissions = app.config['ADMIN_CLAIMS']
        elif user_role == Login.Role.EDITOR.value:
            permissions = app.config['EDITOR_CLAIMS']

        return {
            "claims": permissions,
            "is_super_admin": user_role == Login.Role.ADMIN.value
        }

    @login.user_loader
    def load_user(user_id):
        return Login.objects(id=user_id).first()

    return db

