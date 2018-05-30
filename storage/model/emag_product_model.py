from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentListField, StringField, DateTimeField, ListField, FloatField, IntField
import datetime

from product_model import Price

class EmagProduct(Document):
    meta = {
        'indexes': [
            {'fields': ['product_id'], 'unique': True},
            {'fields': ['name', 'category'], 'unique': True, }
        ]
    }

    category = StringField(required=True, max_length=200)
    product_id = StringField(required=True, max_length=200)
    name = StringField(required=True,max_length=200)
    link = StringField(required=True, max_length=200)
    created_at = IntField(min_value=0, default=datetime.datetime.utcnow)
    updated_at = IntField(min_value=0, default=datetime.datetime.utcnow)
    prices = EmbeddedDocumentListField(Price)
