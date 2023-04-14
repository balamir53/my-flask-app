import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema

from db import items
from models import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint('items', __name__, description='Operations on items')


@blp.route('/item/<string:item_id>')
class Item(MethodView):
    @blp.response(200, ItemSchema)
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
            
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, data, item_id):
        try:
            item = items[item_id]
            item |= data
            return item, 200
        except KeyError:
            abort(404,message='Item not found')


@blp.route('/item')
class ItemLists(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        '''
        get all the items
        '''
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, data):
        '''
        create item
        '''
        item = ItemModel(**data)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message='Bir hata olustu')

        return item, 201