from flask import Blueprint
user_list_bp = Blueprint('user-list', __name__, url_prefix='/api/user-list')

from application.views.user_list import user_list

