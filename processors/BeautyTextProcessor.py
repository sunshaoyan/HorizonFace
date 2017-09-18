from TextProcessor import TextProcesser
from models import *
from utils import *
from conf import start_day
import json


class BeautyTextProcessor(TextProcesser):
    def __init__(self):
        super(BeautyTextProcessor, self).__init__(r'谁拍的照片颜值最高')

    def process(self, msg, match):
        all_name = []
        for ss in Users.objects():
            all_name.append(ss.name)
        #records = PictureCollections.objects(user=name, stats__exists=True)
        _top_photographer = 'no'
        _top_avg_beauty = 0
        _shot_img_num = 0
        _beauty_temp = 0
        for name in allname:
            records = PictureCollections.objects(user = name)
            total_img_num = PictureCollections(user = name,data__gt =
                    start_day).count()
            
            person_records = {}
            for record in records:
                result = json.loads(record['stats'])
                for p in result['result']:
                    if p['beauty']:
                        _beauty_temp = _beauty_temp + result['beauty']
            _temp = _beauty_temp/float(total_img_num)
            if _temp > _top_avg_beauty:
                _top_avg_beauty = _temp
                _top_photographer = name
                _shot_img_num = total_img_num
        
        total_msg = '{}共拍了{}张照片'.format(name, PictureCollections.objects(user=name, date__gt=start_day).count())
        result_msg = '平均颜值达到%f'%(_top_avg_beauty)
        reply_msg = total_msg + result_msg
        msg.reply(reply_msg)
