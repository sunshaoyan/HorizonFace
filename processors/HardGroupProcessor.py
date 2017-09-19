from TextProcessor import TextProcesser
from models import *
import cv2
import numpy as np
import json
import sys

class HardGroupProcessor(TextProcesser):
    def __init__(self):
        super(HardGroupProcessor, self).__init__(r'@(.*)\s的最强小团体')
        users = Users.objects().only('identity', 'name')
        self.id_to_name = {}
        self.name_to_id = {}
        self.name_map = {}
        self.name_map[''] = 0
        self.id = []
        self.result_ID = ''


        for user in users:
            self.id_to_name[user.identity] = user.name
            self.name_map[user.identity] = 0
            self.name_to_id[user.name] = user.identity






    def process(self, msg, match):
        zh_name = match.groups()[0]
        en_name = self.name_to_id[zh_name]

        list_results = []
        id_results = []
        str_records = PictureCollections.objects(stats__exists=True).only('stats')

        for i in range(str_records.__len__()):
            tmp_result = json.loads(str_records[i]["stats"])

            flag = False
            for index in range(tmp_result["result"].__len__()):
                if tmp_result["result"][index]["identity"] == en_name:
                    flag = True
                    break
            if flag:
                list_results.append(tmp_result)
                id_results.append(str_records[i].id)


        for i in range(list_results.__len__()):
            for j in range(len(list_results[i])):
                str_name = str(list_results[i]["result"][j]["identity"])
                if str_name != en_name:
                    self.name_map[str_name] = self.name_map[str_name] + 1

        max_val = 0
        max_name = ''
        for ele in self.name_map:
            if self.name_map[ele] > max_val and ele != '':
                max_val = self.name_map[ele]
                max_name = ele


        f_en_name = False
        f_max_name = False
        for i in range(str_records.__len__()):
            over_result = json.loads(str_records[i]["stats"])
            for index in range(over_result["result"].__len__()):
                if over_result["result"][index]["identity"] == en_name:
                    f_en_name = True
                if over_result["result"][index]["identity"] == max_name:
                    f_max_name = True
                if f_en_name and f_max_name:
                    break
            if f_en_name and f_max_name:
                self.result_ID = str_records[i].id
                break

        try:
            pic = PictureCollections.objects.get(id=self.result_ID)
            img = np.fromstring(pic['img'], np.uint8)  #kuangrenlian
            img = cv2.imdecode(img, cv2.IMREAD_UNCHANGED)
            path = 'images/{}_beauty.jpg'.format(pic.id)  #保存
            cv2.imwrite(path, img)
            msg.reply(en_name + " & " + max_name + " 为最强小团体")
            msg.reply_image(path)           
        except PictureCollections.DoesNotExist:
            msg.reply("The picture is not found.")

