from flask import Flask, request, render_template
from db import stores, items
import uuid

app = Flask(__name__)

# stores = [
#     {
#         'name': 'My Store',
#         'items': [
#             {
#                 'name' : 'my item',
#                 'my price': 15.99
#             }
#         ]
#     }
# ]

@app.get('/store')
def get_stores():
    '''
    get all the stores
    '''
    return {'stores':list(stores.values())}

@app.get('/item')
def get_items():
    '''
    get all the items
    '''
    return {'items':list(items.values())}

@app.post('/store')
def create_store():
    '''
    create a new store
    '''
    data = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {**data, 'id':store_id}
    stores[store_id] = new_store
    
    return new_store, 201

@app.post('/item')
def create_item():
    '''
    create new item
    '''
    data = request.get_json()
    if data['store_id'] not in stores:
        return {'message':'Store not found'},404
    
    item_id = uuid.uuid4().hex
    new_item = {**data, 'id':item_id}
    items[item_id] = new_item
    return new_item, 201

@app.get('/store/<string:store_id>')
def get_store(store_id):
    '''
    get specific store by its id
    '''
    try:
        return stores[store_id]
    except KeyError:
        return {'message':'Store not found'}, 404

@app.get('/item/<string:item_id>')
def get_item_in_store(item_id):
    '''
    get specific item
    '''
    try:
        return items[item_id]
    except KeyError:
        return {'message':'Item not found'}, 404

@app.route('/<string:name>')
@app.route('/index')
def index(name):
    # name = 'Rosalia'
    return render_template('index.html', title='Welcome', username=name)