from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentListField, StringField, DateTimeField, ListField, FloatField
import datetime

class Product(Document):
    title = StringField(required=True, max_length=200)
    category = StringField(required=True, max_length=200)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    update_at = DateTimeField(default=datetime.datetime.utcnow)
    prices = EmbeddedDocumentListField(Price)
    today_price = FloatField(min_value=0.0)

class Price(EmbeddedDocument):
    timestamp = DateTimeField(default=datetime.datetime.utcnow)
    value = FloatField(min_value=0.0)
