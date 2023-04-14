import uuid
from flask import request
from db import stores
from db import db
from sqlalchemy.exc import SQLAlchemyError

from flask_smorest import Blueprint, abort
from flask.views import MethodView
from models import StoreModel

from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route('/store/<string:store_id>')
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {'message':'Store deleted'}

@blp.route('/store')
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        '''
        get all the stores
        '''
        return StoreModel.query.all()
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self,data):
        '''
        create a new store
        '''

        new_store = StoreModel(**data)

        try:
            db.session.add(new_store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message='Bir hata olustu')

        return new_store, 201