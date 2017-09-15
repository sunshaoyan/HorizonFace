import inspect
import processors

class TextParser():
    """docstring for TextParser"""
    def __init__(self, msg):
        self.processors = []
        for l in inspect.getmembers(processors, inspect.isclass):
            c = getattr(processors, l[0])
            self.register_processor(c(msg))

    def register_processor(self, processor):
        self.processors.append(processor)

    def parse_text(self, text):
        for processor in self.processors:
            if processor.match(text):
                break