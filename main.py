# -*- coding:utf-8 -*-
from TextParser import TextParser
import cv2

"""
A class simulating the wechat message
"""
class Message():
    def __init__(self, text):
        self.text = text

    def reply(self, text):
        print("REPLYING: {}".format(text))

    def reply_image(self, path):
        img = cv2.imread(path)
        cv2.imshow('image', img)
        cv2.waitKey()
        cv2.destroyAllWindows()


tp = TextParser()

while True:
    text = input('请输入消息(输入q退出):')
    if text == 'q':
        break
    msg = Message(text)
    tp.parse_text(msg)
