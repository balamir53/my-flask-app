from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token

from db import db
from models import UserModel
from schemas import UserSchema

blp = Blueprint('Users', __name__, description='Operations on users')

@blp.route('/register')
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, data):
        
        user = UserModel(username=data['username'],
            password=pbkdf2_sha256.hash(data['password'])
        )

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message='some error occured')

        return {'message': 'User created successfully'}, 201

@blp.route('/login')
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, data):
        user = UserModel.query.filter(UserModel.username == data['username']).first()

        if user and pbkdf2_sha256.verify(data['password'], user.password):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200
        
        abort(401, message='Yanlis hesap bilgisi girdiniz')