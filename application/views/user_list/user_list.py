from application.services import BackendError, AuthenticationException, AuthorizationException
from application.services.auth import user_logged_in
from application.services.user_list import validate_create_user, validate_update_user, generate_fake_users
from application.views.user_list import user_list_bp
from application.models import User
from flask import jsonify, request


@user_list_bp.route('/users', methods=['GET'])
def get_users():
    try:
        @user_logged_in(require_claims="view:user")
        def _get_users():
            if not User.objects():
                _ = [User(**u).save() for u in generate_fake_users()]
            return jsonify({
                'users': [
                    u.to_dict() for u in User.objects()
                ]
            })
        return _get_users()
    except AuthorizationException as e:
        return jsonify({'error_message': str(e)}), 403
    except AuthenticationException as e:
        return jsonify({'error_message': str(e)}), 401


@user_list_bp.route('/users/<uid>', methods=['GET'])
def get_user(uid):
    try:
        @user_logged_in(require_claims="view:user")
        def _get_user():
            if u := User.objects(id=uid).first():
                return jsonify({
                    'users': u.to_dict()
                })
            raise BackendError("User not found")
        return _get_user()
    except AuthorizationException as e:
        return jsonify({'error_message': str(e)}), 403
    except AuthenticationException as e:
        return jsonify({'error_message': str(e)}), 401
    except BackendError as e:
        return jsonify({'error_message': str(e)}), 404


@user_list_bp.route('/users', methods=['POST'])
def create_user():
    try:
        @user_logged_in(require_claims="edit:user")
        def _create_user():
            validate_create_user(request.json.get('data', request.json))
            return jsonify({
                'users': User(**request.json.get('data', request.json)).save().reload().to_dict()
            }), 201
        return _create_user()
    except AuthorizationException as e:
        return jsonify({'error_message': str(e)}), 403
    except AuthenticationException as e:
        return jsonify({'error_message': str(e)}), 401
    except BackendError as e:
        return jsonify({'error_message': str(e)}), 404


@user_list_bp.route('/users/<uid>', methods=['PUT'])
def update_user(uid):
    try:
        @user_logged_in(require_claims="edit:user")
        def _update_user():
            if u := User.objects(id=uid).first():
                validate_update_user(request.json)
                u.modify(**request.json)
                return jsonify({'users': u.to_dict()})
            return jsonify({'error_message': 'User not found'}), 404
        return _update_user()
    except AuthorizationException as e:
        return jsonify({'error_message': str(e)}), 403
    except AuthenticationException as e:
        return jsonify({'error_message': str(e)}), 401
    except BackendError as e:
        return jsonify({'error_message': str(e)}), 404


@user_list_bp.route('/users/<uid>', methods=['DELETE'])
def delete_item(uid):
    try:
        @user_logged_in(require_claims="remove:user")
        def _delete_user():
            if u := User.objects(id=uid).first():
                u.delete()
                return jsonify({'users': {'deleted': True}})
            return jsonify({'error_message': 'User not found'}), 404
        return _delete_user()
    except AuthorizationException as e:
        return jsonify({'error_message': str(e)}), 403
    except AuthenticationException as e:
        return jsonify({'error_message': str(e)}), 401
    except BackendError as e:
        return jsonify({'error_message': str(e)}), 404


