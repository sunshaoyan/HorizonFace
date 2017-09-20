from TextProcessor import TextProcesser
from models import *
from utils import *
from conf import start_day
import json


class BeautyTextProcessor(TextProcesser):
    def __init__(self):
        super(BeautyTextProcessor, self).__init__(r'谁拍的照片颜值最高')

    def process(self, msg, match):
        dict_num = {}
        dict_beauty = {}
        records = PictureCollections.objects(stats__exists=True).only('user', 'stats')
        for record in records:
            r = json.loads(record['stats'])
            for result in r['result']:
                if 'beauty' in result:
                    dict_num[record['user']] = dict_num[record['user']] + 1 if record['user'] in dict_num else 1
                    dict_beauty[record['user']] = dict_beauty[record['user']] + result['beauty'] if record['user'] in dict_beauty else 1

        for x in dict_num:
            dict_beauty[x] = dict_beauty[x] / dict_num[x]
        max_key = keywithmaxval(dict_beauty)
        reply_msg = '{}拍的照片中，人脸的平均颜值最高，高达{}'.format(max_key, dict_beauty[max_key])
        msg.reply(reply_msg)