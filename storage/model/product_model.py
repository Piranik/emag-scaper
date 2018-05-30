from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentListField, StringField, DateTimeField, ListField, FloatField, IntField
import datetime

class Price(EmbeddedDocument):
    start_timestamp = IntField(required=True, min_value=0, default=datetime.datetime.utcnow)
    finish_timestamp = IntField(required=True, min_value=0, default=datetime.datetime.utcnow)
    value = FloatField(min_value=0.0)

