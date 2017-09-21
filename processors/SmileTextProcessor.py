from TextProcessor import TextProcesser
from models import *
from utils import *
from conf import start_day
import json
from models import *
from utils import *
from conf import start_day
import json


class SmileTextProcessor(TextProcesser):
    def __init__(self):
        super(SmileTextProcessor, self).__init__(r'谁拍的照片笑脸最多')

    def process(self, msg, match):
        _top_photographer = 'no'
        _top_smile_num = 0

        dict = { }
        records = PictureCollections.objects(stats__exists=True).only('user', 'stats')
        for record in records:
            r = json.loads(record['stats'])
            for result in r['result']:
                if 'expression' in result:
                    if result['expression'] > 0:
                        dict[record['user']] = dict[record['user']] + 1 if record['user'] in dict else 1
                        if dict[record['user']] > _top_smile_num:
                            _top_smile_num = dict[record['user']]
                            _top_photographer = record['user']

        total_msg = '{}共拍了{}张照片'.format(_top_photographer, PictureCollections.objects(user=_top_photographer).count())
        result_msg = '共有%d张笑脸' % (_top_smile_num)
        reply_msg = total_msg + result_msg
        msg.reply(reply_msg)