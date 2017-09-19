from TextProcessor import TextProcesser
from models import *
from utils import *
from conf import start_day
import json


class LikeTextProcessor(TextProcesser):
    def __init__(self):
        super(LikeTextProcessor, self).__init__(r'@(.*)\s最中意谁')#..匹配数据  \s空格

    def process(self, msg, match):
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
            max_key = keywithmaxval(person_records)
            try:
                user = Users.objects.get(identity=max_key)   #获得用户名
                result_msg = '其中{}张都有{}'.format(person_records[max_key], user.name)
            except:
                pass
        reply_msg = total_msg + result_msg
        msg.reply(reply_msg)