from marshmallow import Schema, fields

class ItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)
    store = fields.Nested(lambda:StoreSchema(only=('id','name')), dump_only=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()

class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    items = fields.List(fields.Nested(ItemSchema(exclude=('store',))), dump_only=True)
    tags = fields.List(fields.Nested(lambda:TagSchema(exclude=('store',))), dump_only=True)

class TagSchema(Schema):
    id=fields.Int(dump_only=True)
    name = fields.Str(required=True)
    store_id=fields.Int(load_only=True)
    store = fields.Nested(StoreSchema(only=('id','name')), dump_only=True)

