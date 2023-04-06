from flask import Blueprint
redis_task_bp = Blueprint('redis-task', __name__, url_prefix='/api/redis-task')

from application.views.redis_task import redis_task