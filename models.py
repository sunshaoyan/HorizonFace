from mongoengine import *
import datetime

#connect('entrance_guard_usa', host='mongodb://10.31.32.139:27017')
#connect('entrance_guard_usa', host='mongodb://114.55.27.91:27018')192.16
connect('entrance_guard_usa', host='mongodb://192.168.43.118:27017')


class PictureCollections(Document):   #json数组  按照照片数
    date = DateTimeField()   #上传日期
    user = StringField()     #摄影师 群昵称
    img = BinaryField()    #原始图像 图像二进制编码 看decode
    stats = StringField()   #json字符串 所有源数据 格式在readme  reload0.g...  user 三个字段 邮箱id  kai.yu
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

class Occurences(Document):   #一个人脸框一个记录
    identity = StringField()  #kai.yu
    location = EmbeddedDocumentField('Location') 
    img = BinaryField()
    expression = IntField()   #表情
    age = FloatField()
    race = StringField()  #人种
    gender = StringField()
    glasses = IntField()
    beauty = FloatField()
    photographer = StringField()   #上传者
    date = DateTimeField()    #上传时间
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
