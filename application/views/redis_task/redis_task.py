import json
import requests
import redis
from application.services import BackendError
from application.views.redis_task import redis_task_bp
from flask import jsonify

redis_client = redis.Redis(host='localhost', port=6379, db=0)


@redis_task_bp.route('/w-redis', methods=['GET'])
def with_redis():

    cached_response = redis_client.get('comments_1')
    if cached_response is not None:
        json_response = json.loads(cached_response)
        return jsonify(json_response)

    url = 'https://jsonplaceholder.typicode.com/comments'
    response = requests.get(url)
    json_response = response.json()

    redis_client.setex('comments_1', 10, json.dumps(json_response))
    return jsonify(json_response)


@redis_task_bp.route('/wo-redis', methods=['GET'])
def without_redis():
    url = 'https://jsonplaceholder.typicode.com/comments'
    response = requests.get(url)
    json_response = response.json()
    return jsonify(json_response)




