from flask import Blueprint

login_auth_bp = Blueprint('login-auth', __name__, url_prefix='/api/login-auth')

from application.views.login_auth import login_auth
