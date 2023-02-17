from application.services import BackendError
from application.services.user_list import validate_create_user, validate_update_user, generate_fake_users
from application.views.user_list import user_list_bp
from application.models import User
from flask import jsonify, request


@user_list_bp.route('/users', methods=['GET'])
def get_users():

    if not User.objects():
        _ = [User(**u).save() for u in generate_fake_users()]
    return jsonify({
        'users': [
            u.to_dict() for u in User.objects()
        ]
    })


@user_list_bp.route('/users/<uid>', methods=['GET'])
def get_user(uid):
    try:
        if u := User.objects(id=uid).first():
            return jsonify({
                'users': u.to_dict()
            })
        raise BackendError("User not found")
    except BackendError as e:
        return jsonify({'error_message': str(e)}), 404


@user_list_bp.route('/users', methods=['POST'])
def create_user():
    try:
        validate_create_user(request.json.get('data', None))
    except BackendError as e:
        return jsonify({'error_message': str(e)}), 404
    return jsonify({
        'users': User(**request.json).save().to_dict()
    }), 201


@user_list_bp.route('/users/<uid>', methods=['PUT'])
def update_user(uid):
    if u := User.objects(id=uid).first():
        try:
            validate_update_user(request.json)
        except BackendError as e:
            return jsonify({'error_message': str(e)}), 404
        u.modify(**request.json)
        return jsonify({'users': u.to_dict()})
    return jsonify({'error_message': 'User not found'}), 404


@user_list_bp.route('/users/<uid>', methods=['DELETE'])
def delete_item(uid):
    if u := User.objects(id=uid).first():
        u.delete()
        return jsonify({'users': {'deleted': True}})
    return jsonify({'error_message': 'User not found'}), 404
