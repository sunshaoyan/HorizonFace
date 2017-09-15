from wxpy import *
from models import *
from utils import *
from TextParser import TextParser
import cv2
from datetime import datetime
from time import sleep
import threading
import base64
import httplib2
import urllib
import json
import hashlib

bot = Bot(cache_path=True)
chat_group = ensure_one(bot.groups().search('HorizonFace'))

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

                try:
                    tpc = PictureCollections.objects.get(md5=md5)
                    self.msg.reply('这张照片已经发过啦')
                except PictureCollections.DoesNotExist:
                    pc = PictureCollections.objects.get(id=str(self.pid))
                    pc.md5 = md5
                    pc.stats = json.dumps(ct_hf)
                    pc.img = bytearray(buf)
                    pc.save()
                    reply_msg = ""
                    for ct_res in ct_hf['result']:
                        identity = ct_res['identity']
                        if not ct_res['identity']:
                            identity = 'unknown'
                        oc = Occurences(
                            identity=identity,
                            photographer=self.msg.member.name,
                            location=Location(
                                left=ct_res['location']['left'],
                                top=ct_res['location']['top'],
                                width=ct_res['location']['width'],
                                height=ct_res['location']['height']
                            )
                        )
                        dict = oc.to_mongo()
                        if 'expression' in ct_res:
                            oc.expression = ct_res['expression']
                            oc.race = ct_res['race']
                            oc.glasses = ct_res['glasses']
                            oc.beauty = ct_res['beauty']
                            oc.age = ct_res['age']
                            dict['expression'] = ct_res['expression']
                            dict['race'] = ct_res['race']
                            dict['glasses'] = ct_res['glasses']
                            dict['beauty'] = ct_res['beauty']
                            dict['age'] = ct_res['age']
                        reply_msg += json.dumps(dict, ensure_ascii=False)
                        oc.img = bytearray(buf)
                        oc.save()
                    self.msg.reply(reply_msg)
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


@bot.register(chat_group, TEXT)
def process_text_msg(msg):
    print(msg)
    tp = TextParser(msg)
    tp.parse_text(msg.text)

bot.join()
