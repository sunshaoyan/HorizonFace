import re

class TextProcesser():
    def __init__(self, pattern_str, msg):
        self.pattern = re.compile(pattern_str)
        self.msg = msg

    def match(self, text):
        match = self.pattern.match(text)
        if match:
            self.process(match)
            return True
        return False

    def process(self, match):
        pass

