from TextParser import TextParser

class Message():
    def __init__(self, text):
        self.text = text

    def reply(self, text):
        print("REPLYING: {}".format(text))

while True:
    text = input('请输入消息(输入q退出):')
    if text == 'q':
        break
    msg = Message(text)
    tp = TextParser(msg)
    tp.parse_text(msg.text)