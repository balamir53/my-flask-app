from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError

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