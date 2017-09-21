from TextProcessor import TextProcesser
from models import *
from utils import *
import json


class GlassesNumberProcessor(TextProcesser):
    def __init__(self):
        super(GlassesNumberProcessor, self).__init__(r'戴眼镜的(.+)有多少')
        print('registered')

    def process(self, msg, match):
        if match.groups()[0] == '人':
            records =  Occurences.objects(glasses=1).only('identity')
        elif match.groups()[0] == '男生':
            records = Occurences.objects(gender='male',glasses=1).only('identity')
        elif match.groups()[0] == '女生':
            records = Occurences.objects(gender='female',glasses=1).only('identity')
        else:
            return
        person_records = {}
        for record in records:
            if record['identity'] and record['identity'] != 'unknown' and record['identity'] not in person_records:
                person_records[record['identity']] = 1
        glassesnumber = len(person_records)
        reply_msg = '戴眼镜的{}有{}个'.format(match.groups()[0], glassesnumber)
        msg.reply(reply_msg)
