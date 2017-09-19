from mongoengine import *
import datetime

# connect('entrance_guard_usa', host='mongodb://104.225.144.56:27017')
# connect('entrance_guard_usa', host='mongodb://114.55.27.91:27018')
connect('entrance_guard_usa', host='mongodb://192.168.43.118:27017')


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
    sex = StringField()
    meta = {
        'strict': False,
        'indexes': [
            '#identity'
        ]
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
    gender = StringField()
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
