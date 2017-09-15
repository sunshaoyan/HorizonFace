from wxpy import *
from mongoengine import *
import cv2
from datetime import datetime, timezone
from time import sleep
import threading
import base64
import httplib2
import urllib
import json
import pdb
import hashlib
import re

bot = Bot(cache_path=True)
chat_group = ensure_one(bot.groups().search('HorizonFace'))

connect('entrance_guard_usa', host='mongodb://10.31.32.139:27017')

start_day = datetime(2017,9,10, tzinfo = timezone.utc)


class PictureCollections(Document):
    date = DateTimeField()
    user = StringField()
    img = BinaryField()
    stats = StringField()
    md5 = StringField()
    meta = {
        'strict': False
    }

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
    location = EmbeddedDocumentField(Location)
    img = BinaryField()
    expression = IntField()
    race = StringField()
    glasses = IntField()
    beauty = FloatField()
    meta = {
        'strict': False
    }


def overlap(bbox1, bbox2):
    area1 = bbox1["width"] * bbox1["height"]
    area2 = bbox2["width"] * bbox2["height"]
    x1 = max(bbox1["left"], bbox2["left"])
    y1 = max(bbox1["top"], bbox2["top"])
    x2 = min(bbox1["left"] + bbox1["width"], bbox2["left"] + bbox2["width"])
    y2 = min(bbox1["top"] + bbox1["height"], bbox2["top"] + bbox2["height"])
    area_o = (x2-x1) * (y2-y1)
    if x2 < x1 or y2 < y1:
        area_o = 0
    return area_o / min(area1, area2)

def merge_ct(ct_hf, ct_bd):
    for ct_hf_item in ct_hf["result"]:
        for ct_bd_item in ct_bd["result"]:
            if overlap(ct_hf_item["location"], ct_bd_item["location"]) > 0.5:
                for key in ct_bd_item.keys():
                    ct_hf_item[key] = ct_bd_item[key]

class ProcessThread(threading.Thread):

    def __init__(self, img_path, msg, pid):
        threading.Thread.__init__(self)
        self.img_path = img_path
        self.msg = msg
        self.pid = pid
        self.token = '24.08e52160dfa5b2853275bd8452ff0ffc.2592000.1507381317.282335-10108825'

    def run(self):
        sleep(12)
        with open(self.img_path, 'rb') as image_file:
            try:
                img = cv2.imread(self.img_path)
                max_size = 1920
                if img.shape[0] > max_size or img.shape[1] > max_size:
                    scale = max_size / max(img.shape[0], img.shape[1])
                    size = (int(img.shape[1]*scale), int(img.shape[0]*scale))
                    img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
                r,buf=cv2.imencode('.jpg',img)
                img_str=base64.b64encode(bytearray(buf))

                md5 = hashlib.md5(image_file.read()).hexdigest()

                url = 'http://10.31.32.139:8081/predict_image_str'
                body = {'image': img_str}
                headers = {'Content-type': 'application/x-www-form-urlencoded'}
                http = httplib2.Http()
                response, content = http.request(url, 'POST', headers=headers, body=urllib.parse.urlencode(body))
                ct = json.loads(content.decode('ascii'))
                ct_hf = ct['data']
                img_ret = ct['image']
                new_path = self.img_path[:-4] + "_a.jpg"
                with open(new_path, 'wb') as fh:
                    fh.write(base64.decodebytes(img_ret.encode('ascii')))

                params = {"max_face_num": 30, "face_fields": "age,beauty,expression,faceshape,gender,glasses,race","image": img_str}
                url = "https://aip.baidubce.com/rest/2.0/face/v1/detect"
                url = url + "?access_token=" + self.token
                headers = {'Content-type': 'application/x-www-form-urlencoded'}
                http = httplib2.Http()
                response, content = http.request(url, 'POST', headers=headers, body=urllib.parse.urlencode(params))
                ct_bd = json.loads(content.decode('ascii'))

                merge_ct(ct_hf, ct_bd)

                chat_group.send_image(new_path)
                # chat_group.send_msg(ct_hf)

                try:
                    tpc = PictureCollections.objects.get(md5=md5)
                except PictureCollections.DoesNotExist:
                    pc = PictureCollections.objects.get(id=str(self.pid))
                    pc.md5 = md5
                    pc.stats = json.dumps(ct_hf)
                    pc.img = bytearray(buf)
                    pc.save()
                except Exception as e:
                    print(e)
            except Exception as e:
                print(e)

@bot.register(chat_group, PICTURE)
def process_img_msg(msg):
    pc = PictureCollections()
    pc.date = datetime.utcnow()
    pc.user = msg.member.name
    pc.save()
    print(pc.id)
    file_name = "images/" + str(pc.id) + ".jpg"
    print(file_name)
    msg.get_file(file_name)
    msg.reply('收到@'+msg.member.name+' 发的一张靓照')
    th = ProcessThread(file_name, msg, pc.id)
    th.start()


class TextProcesser():
    def __init__(self, pattern_str, msg):
        self.pattern = re.compile(pattern_str)
        self.msg = msg

    def match(self, text):
        match = self.pattern.match(text)
        if match:
            self.process(match)
            return True
        return False

    def process(self, match):
        pass

class LikeTextProcessor(TextProcesser):
    def __init__(self, msg):
        super(LikeTextProcessor, self).__init__(r'@(.*)\s最中意谁', msg)

    def process(self, match):
        name = match.groups()[0]
        records = PictureCollections.objects(user=name, stats__exists=True)
        total_msg = '{}共拍了{}张照片'.format(name, PictureCollections.objects(user=name, date__gt=start_day).count())
        result_msg = '，结果谁都没有拍到过'
        person_records = {}
        for record in records:
            result = json.loads(record['stats'])
            for p in result['result']:
                if p['identity']:
                    person_records[p['identity']] = person_records[p['identity']] + 1 if p['identity'] in person_records else 1
        if person_records:
            max_key = self.keywithmaxval(person_records)
            try:
                user = Users.objects.get(identity=max_key)
                result_msg = '其中{}张都有{}'.format(person_records[max_key], user.name)
            except:
                pass
        reply_msg = total_msg + result_msg
        self.msg.reply(reply_msg)


    def keywithmaxval(self, d):
        """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
        v=list(d.values())
        k=list(d.keys())
        return k[v.index(max(v))]



class TextParser():
    """docstring for TextParser"""
    def __init__(self, msg):
        self.processors = [LikeTextProcessor(msg)]

    def parse_text(self, text):
        for processor in self.processors:
            if processor.match(text):
                break


@bot.register(chat_group, TEXT)
def process_text_msg(msg):
    tp = TextParser(msg)
    tp.parse_text(msg.text)
    print(msg)

bot.join()
