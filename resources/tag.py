from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel
from schemas import TagSchema

blp = Blueprint('Tags', __name__, description='Operations on tags')

@blp.route('/store/<string:store_id>/tag')
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        '''
        get tags of the store
        '''
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, data, store_id):
        '''
        create a tag in the store
        '''
        if TagModel.query.filter(TagModel.store_id==store_id, TagModel.name==data['name']).first():
            abort(400, message='Bu storeda ayni isimde bir tag var')

        tag = TagModel(**data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message='Error occurred')

        return tag

@blp.route('/tag/<string:tag_id>')
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        '''
        get the tag via its id
        '''
        tag = TagModel.query.get_or_404(tag_id)
        return tag