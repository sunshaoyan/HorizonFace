from TextProcessor import TextProcesser
from models import *
import cv2
import numpy as np


class BeautifulModelProcessor(TextProcesser):
    def __init__(self):
        super(BeautifulModelProcessor, self).__init__(r'颜值最高的人')

    def process(self, msg, match):
        result = Occurences.objects().order_by('-beauty').limit(-1).first()
        name = "不知何许人也"
        if result['identity'] != 'unknown':
            try:
                u = Users.objects.get(identity=result['identity'])
                name = u['name']
            except:
                pass
        reply_msg = '照片中 {} 的颜值最高，高达 {}'.format(name, result['beauty'])
        img = np.fromstring(result['img'], np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_UNCHANGED)
        cv2.rectangle(img,
                      (result['location']['left'], result['location']['top']),
                      (result['location']['left']+result['location']['width'],
                       result['location']['top']+result['location']['height']), (0, 0, 255), 2)
        path = 'images/{}_beauty.jpg'.format(result.id)
        cv2.imwrite(path, img)
        msg.reply(reply_msg)
        msg.reply_img(path)
