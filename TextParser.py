import inspect
import processors


class TextParser():
    """docstring for TextParser"""
    def __init__(self):
        self.processors = []
        for l in inspect.getmembers(processors, inspect.isclass):
            c = getattr(processors, l[0])
            self.register_processor(c())

    def register_processor(self, processor):
        self.processors.append(processor)

    def parse_text(self, msg):
        for processor in self.processors:
            if processor.match(msg):
                break