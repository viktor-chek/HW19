from flask import request

from implemented import user_service
from dao.model.user import UserSchema
from flask_restx import Resource, Namespace


ns_user = Namespace('users')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@ns_user.route('/')
class UsersView(Resource):
    def get(self):
        all_user = user_service.get_all()
        return users_schema.dump(all_user)

    def post(self):
        data = request.json
        user = user_service.create_user(data)
        return "", 201, {"location": f"/users/{user.id}"}


@ns_user.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        user = user_service.get_one(uid)
        return user_schema.dump(user)

    def put(self, uid):
        data = request.json
        data["id"] = uid
        user_service.update(data)
        return "", 204

    def delete(self, uid):
        user_service.delete(uid)
        return "", 204
