import re

class TextProcesser():
    def __init__(self, pattern_str):
        print(pattern_str)
        self.pattern = re.compile(pattern_str)

    def match(self, msg):
        match = self.pattern.match(msg.text)
        if match:
            self.process(msg, match)
            return True
        return False

    def process(self, msg, match):
        pass

