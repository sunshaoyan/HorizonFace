from mongoengine import *
import datetime

connect('entrance_guard_usa', host='mongodb://10.31.32.139:27017')


class PictureCollections(Document):
    date = DateTimeField()
    user = StringField()
    img = BinaryField()
    stats = StringField()
    md5 = StringField()
    meta = {
        'strict': False,
        'indexes': [
            '-date',
            '#user'
        ]
    }

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = datetime.datetime.utcnow()
        return super(PictureCollections, self).save(*args, **kwargs)


class Users(Document):
    identity = StringField()
    name = StringField()
    meta = {
        'strict': False
    }

class Location(Document):
    top = IntField()
    left = IntField()
    width = IntField()
    height = IntField()
    
class Occurences(Document):
    identity = StringField()
    location = EmbeddedDocumentField('Location')
    img = BinaryField()
    expression = IntField()
    age = FloatField()
    race = StringField()
    glasses = IntField()
    beauty = FloatField()
    photographer = StringField()
    date = DateTimeField()
    meta = {
        'strict': False,
        'indexes': [
            '-date',
            '#identity',
            '#photographer'
        ]
    }

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = datetime.datetime.utcnow()
        return super(Occurences, self).save(*args, **kwargs)
