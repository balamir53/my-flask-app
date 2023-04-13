import uuid
from flask import request
from db import stores

from flask_smorest import Blueprint, abort
from flask.views import MethodView

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route('/store/<string:store_id>')
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message='Store not found')
    def delete(self, store_id):
        try:
            temp_store = stores[store_id]
            del stores[store_id]
            return {'message':'Store deleted.', 'deleted_store':temp_store}
        except KeyError:
            abort(404, message='Store not found')

@blp.route('/store')
class StoreList(MethodView):
    def get(self):
        '''
        get all the stores
        '''
        return {'stores':list(stores.values())}
    def post(self):
        '''
        create a new store
        '''
        data = request.get_json()
    
        if 'name' not in data:
            abort(400,
                message = 'Bad request. Lutfen "name" parametresini de girin'
            )
    
        for store in stores.values():
            if data['name'] == store['name']:
                abort(400, message='Bu isimde zaten bir dukkan var')
        
        store_id = uuid.uuid4().hex
        new_store = {**data, 'id':store_id}
        stores[store_id] = new_store
        
        return new_store, 201