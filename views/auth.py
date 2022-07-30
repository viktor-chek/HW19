from flask import request
from implemented import auth_service

from flask_restx import Resource, Namespace

ns_auth = Namespace('auth')

@ns_auth.route('/')
class AuthViews(Resource):
    def post(self):
        data = request.json

        username = data.get('username')
        password = data.get('password')

        if None in [username, password]:
            return "", 400

        tokens = auth_service.generate_tokens(username, password)

        return tokens, 201

    def put(self):
        data = request.json
        token = data.get('refresh_token')

        tokens = auth_service.approve_refresh_token(token)

        return tokens, 201
