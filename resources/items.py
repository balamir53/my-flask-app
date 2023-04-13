import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import items

blp = Blueprint('items', __name__, description='Operations on items')


@blp.route('/item/<string:item_id>')
class Item(MethodView):
    def get(self, item_id):
        '''
        get specific item via its id
        '''
        try:
            return items[item_id]
        except KeyError:
            abort(404, message='item not found')
    def delete(self, item_id):
        '''
        delete an item
        '''
        try:
            del items[item_id]
            return {'message':'Item deleted.'}
        except KeyError:
            abort(404, message='Item not found')
    def put(self, item_id):
        data = request.get_json()
        if 'price' not in data or 'name' not in data:
            abort(400, message='Lutfen price ya da name parametresini girin')
        try:
            item = items[item_id]
            item |= data
            return item, 200
        except KeyError:
            abort(404,message='Item not found')


@blp.route('/item')
class ItemLists(MethodView):
    def get(self):
        '''
        get all the items
        '''
        return {'items':list(items.values())}

    def post(self):
        '''
        create item
        '''
        data = request.get_json()
        if ( 'price' not in data
            or 'store_id' not in data
            or 'name' not in data):
            abort(400, message= 'Lutfen verinin icinde price, store_id ve name oldugundan emin olun')
        
        for item in items.values():
            if (data['name'] == item['name'] and
                data['store_id'] == item['store_id']):
                abort(400, message='Bu dukkanda zaten o malzeme var')
        
        item_id = uuid.uuid4().hex
        new_item = {**data, 'id':item_id}
        items[item_id] = new_item
        return new_item, 201