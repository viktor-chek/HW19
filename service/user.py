import base64
import hashlib
import hmac

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_by_username(self, username):
        return self.dao.get_by_username(username)

    def create_user(self, data):
        data["password"] = self.generate_password(data["password"])

        return self.dao.create_user(data)

    def generate_password(self, password):
        """Функция кодирования пароля в hash"""
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return base64.b64encode(hash_digest)

    def update(self, uid):
        uid['password'] = self.generate_password(uid["password"])
        self.dao.update(uid)

        return uid

    def delete(self, uid):
        self.dao.delete(uid)

    def compare_passwords(self, hash_password, password):
        """Функция сверки hash паролей"""
        decoded_digest = base64.b64decode(hash_password)

        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return hmac.compare_digest(decoded_digest, hash_digest)
