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

