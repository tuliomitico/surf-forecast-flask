import typing as t

from flask_jwt_extended import create_access_token, decode_token
from passlib.hash import bcrypt

class AuthService():
    
    @staticmethod
    def compare_password(password: str, hashed_password: str) -> bool:
        return bcrypt.verify(password,hashed_password)
    
    @staticmethod
    def hash_password(password: str, salt: int = 10) -> str:
        return bcrypt.using(rounds=salt).hash(password)
    
    @staticmethod
    def generate_token(payload) -> str:
        return create_access_token(identity=payload)

    @staticmethod
    def decode_token(token: str) -> t.Dict:
        return decode_token(token,)['id']