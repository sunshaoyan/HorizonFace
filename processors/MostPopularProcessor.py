from TextProcessor import TextProcesser
from models import *
from utils import *
import json

class MostPopularProcessor(TextProcesser):
    def __init__(self):
        super(MostPopularProcessor, self).__init__(r'.*交际花.*')
        self.all_person = {}
        self.max_num = 0
        self.max_index = 0
        users = Users.objects().only('identity', 'name')
        self.id_to_name = {}
        self.name_to_id = {}
        for user in users:
            self.id_to_name[user.identity] = user.name
            self.name_to_id[user.name] = user.identity
        print('registered')

    def process(self, msg, match):
        # if match.groups()[0] == '人':
        if match:
            str_data = PictureCollections.objects(stats__exists=True).only('stats');
            for person_i in str_data:
                person_records = json.loads(person_i['stats']);
                if len(person_records) != 1:
                    for person_in_pic in person_records["result"]:
                        name = person_in_pic["identity"]
                        if name in self.all_person:
                            for person_add in person_records["result"]:
                                name_to_add = person_add["identity"]
                                if  name_to_add != name:
                                    if name_to_add not in self.all_person[name]:
                                        self.all_person[name].append(name_to_add)
                        else:
                            self.all_person[name] = []
                            for person_add in person_records["result"]:
                                name_to_add = person_add["identity"]
                                if  name_to_add != name:
                                    if name_to_add not in self.all_person[name]:
                                        self.all_person[name].append(name_to_add)
        for i in self.all_person:
            if i != "":
                if len(self.all_person[i]) > self.max_num:
                    self.max_num = len(self.all_person[i])
                    self.max_index = i
        reply_msg = '所有照片中 {} 是交际花，TA和团队中 {} 个人同框过'.format(self.id_to_name[self.max_index], self.max_num)
        msg.reply(reply_msg)
