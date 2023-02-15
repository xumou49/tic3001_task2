from application.services import BackendError
from application.services.login_auth import validate_login
from application.views.login_auth import login_auth_bp
from application.models.login import Login
from flask import jsonify, request
from flask_jwt_extended import create_access_token


@login_auth_bp.route('/login', methods=['POST'])
def login():
    username, password = request.json.get('username', None), request.json.get('password', None)
    if not (username and password):
        raise BackendError("Credentials is not provided")

    if login_user := validate_login(username, password):
        return jsonify({'access_token': create_access_token(login_user)}), 200
    else:
        return jsonify({'error_message': 'The login user is not authenticated'}), 200
