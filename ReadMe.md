# Horizon Face

This project is for automatically collecting and analysing photos within a wechat chatgroup.

## Dependencies

1. wxpy : serves as a robot to collect photos and reply messages
2. mongoengine : provides interaction with the database
3. (private) C++ server: provides face detection and recognition
4. Baidu Face API: provides face detection and attributes analysis

## Development

We provide development kit to parse text messages as commands that request some statistic data.
To develop your own parser, you could follow these steps:

1. Create a file in ``processors/`` folder (e.g. ``LikeTextProcessor.py``)
2. Declare a class as the subclass of TextProcessor:

```python
from TextParser import TextParser

class LikeTextProcessor(TextParser):
    def __init__(self, msg):
        # register a reg-expression here for the command
        super(LikeTextProcessor, self).__init__(r'@(.*)\s最中意谁', msg)
        
    def process(self, match):
        # match is the match for the reg-expression
        
        # DO your statistics
        
        self.msg.reply('your reply text')
        self.msg.reply_img('your image path') # you can get some image from the database and edit it with cv2
```

3. Register the class in the module init file ``processors/__init__.py`` by first import it and then add the name to ``__all__`` array.

```python
from .LikeTextProcessor import LikeTextProcessor

__all__= [
    'LikeTextProcessor',
]
```

4 Test your code by running

```bash
$ python3 main.py
```

and input your test command.

## Important

PLEASE test with ``main.py`` rather than ``bot.py`` which is for production use, because frequent request of wechat login may cause account locking!!!