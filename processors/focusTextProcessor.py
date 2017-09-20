from TextProcessor import TextProcesser
from models import *
from utils import *
from conf import start_day
import json
import sklearn

class smileTextProcessor(TextProcesser):
    def __init__(self):
        super(smileTextProcessor, self).__init__(r'谁对着镜头姿态最固定')

    def process(self, msg, match):
        all_name = []
        for ss in Users.objects():
            all_name.append(ss.name)
        _top_photographer = 'no'
        _top_smile_num = 0
        _pitch = 0
        _yaw = 0
        _roll = 0
        for name in allname:
            records = Occurrences.objects(user = name)
            total_img_num = Occurrences.objects(user = name,data__gt =
                    start_day).count()
            _smile_num_temp = 0
            for record in records:
                result = json.loads(record['stats'])
                for p in result['expression']:
                    if p['expression'] == 2 or p['expression'] == 1:
                         _smile_num_temp = _smile_num_temp + 1
            if _smile_num_temp > _top_smile_num:
                _top_smile_num = _smile_num_temp
                _top_photographer = name
        
        total_msg = '{}共拍了{}张照片'.format(name, PictureCollections.objects(user=name, date__gt=start_day).count())
        result_msg = '共有%d张笑脸'%(_top_smile_num)
        reply_msg = total_msg + result_msg
        msg.reply(reply_msg)
