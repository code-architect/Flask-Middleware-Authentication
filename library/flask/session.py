from bson.json_util import dumps
from flask import Response, request


class FlaskSession:
    @staticmethod
    def get():
        print(request.environ['auth_token'])
        print(request.environ['auth_success'])
        print(request.environ['session_id'])

        return Response(dumps({
            'status': 'ok',
            'data': 'ok',
            "code": 200
        }), mimetype='text/json'), 200

    @staticmethod
    def update():
        pass
