from TextProcessor import TextProcesser
from time import sleep


class LovelyProcessor(TextProcesser):
    def __init__(self):
        super(LovelyProcessor, self).__init__(r'谁是最可爱的人')

    def process(self, msg, match):
        msg.reply_image('img/hr.jpg')
        sleep(10)
        msg.reply('哦，忘了，还有这位:')
        sleep(1)
        msg.reply_image('img/kai.jpg')