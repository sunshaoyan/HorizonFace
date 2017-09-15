# Horizon Face

This project is for automatically collecting and analysing photos within a wechat chatgroup.

## Dependencies

1. [wxpy](http://wxpy.readthedocs.io/zh/latest/index.html) : serves as a robot to collect photos and reply messages
2. [mongoengine](http://docs.mongoengine.org/apireference.html) : provides interaction with the database
3. (private) C++ server: provides face detection and recognition
4. [Baidu Face API](https://cloud.baidu.com/doc/FACE/Face-API.html#.E4.BA.BA.E8.84.B8.E6.A3.80.E6.B5.8B): provides face detection and attributes analysis

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

## Database

The database format is as declared in ``models.py``.

### ``PictureCollections``
One document in this collection corresponds to one uploaded image.

```date``` field is the upload time.

```user``` field is the photographer (wechat name).

```md5``` field is used to exclude duplicate images.

```img``` field is the raw image in binary.

``stats`` field is the raw json of the analysis result, such as:

```json
{"result": [
{"gender": "male", "pitch": 1.0520080327988, "race": "yellow", "location": {"top": 328, "left": 183, "height": 68, "width": 79}, "expression_probablity": 0.8709254860878, "race_probability": 0.99973601102829, "rotation_angle": -2, "gender_probability": 0.99991512298584, "glasses": 1, "age": 32.630474090576, "roll": -4.9296202659607, "identity": "yishan.zhang", "glasses_probability": 0.99987423419952, "face_probability": 1, "beauty": 26.279113769531, "yaw": -13.995768547058, "expression": 1, "faceshape": [{"probability": 0.053247287869453, "type": "square"}, {"probability": 0.05485212802887, "type": "triangle"}, {"probability": 0.10603010654449, "type": "oval"}, {"probability": 0.0053467354737222, "type": "heart"}, {"probability": 0.78052371740341, "type": "round"}]}, 
{"gender": "female", "pitch": 0.82871550321579, "race": "yellow", "location": {"top": 485, "left": 15, "height": 94, "width": 101}, "expression_probablity": 0.98333412408829, "race_probability": 0.99998557567596, "rotation_angle": 3, "gender_probability": 0.99999010562897, "glasses": 1, "age": 25.832576751709, "roll": 1.7325274944305, "identity": "yuting.liu", "glasses_probability": 0.9995750784874, "face_probability": 1, "beauty": 44.97737121582, "yaw": -13.487314224243, "expression": 1, "faceshape": [{"probability": 0.048728778958321, "type": "square"}, {"probability": 0.20114889740944, "type": "triangle"}, {"probability": 0.017348473891616, "type": "oval"}, {"probability": 0.039832547307014, "type": "heart"}, {"probability": 0.69294130802155, "type": "round"}]}, 
{"identity": "ding.liu", "location": {"top": 179, "left": 458, "height": 41, "width": 41}}, 
{"gender": "male", "pitch": 2.9942271709442, "race": "yellow", "location": {"top": 442, "left": 1170, "height": 110, "width": 121}, "expression_probablity": 0.99987399578094, "race_probability": 0.99999988079071, "rotation_angle": 6, "gender_probability": 0.99999988079071, "glasses": 0, "age": 29.096225738525, "roll": 7.8307189941406, "identity": "shaoyan.sun", "glasses_probability": 0.99998927116394, "face_probability": 1, "beauty": 40.45418548584, "yaw": 8.522575378418, "expression": 1, "faceshape": [{"probability": 0.021569181233644, "type": "square"}, {"probability": 0.59955924749374, "type": "triangle"}, {"probability": 0.046120498329401, "type": "oval"}, {"probability": 0.010387846268713, "type": "heart"}, {"probability": 0.3223631978035, "type": "round"}]}, 
{"gender": "male", "pitch": -4.6260681152344, "race": "yellow", "location": {"top": 321, "left": 912, "height": 71, "width": 79}, "expression_probablity": 0.99428832530975, "race_probability": 0.9999783039093, "rotation_angle": -10, "gender_probability": 0.99998164176941, "glasses": 1, "age": 27.871730804443, "roll": -7.0358691215515, "identity": "tingcheng.wu", "glasses_probability": 0.99929440021515, "face_probability": 1, "beauty": 40.989395141602, "yaw": 18.345357894897, "expression": 0, "faceshape": [{"probability": 0.28823563456535, "type": "square"}, {"probability": 0.0194001365453, "type": "triangle"}, {"probability": 0.2190715521574, "type": "oval"}, {"probability": 0.0068779760040343, "type": "heart"}, {"probability": 0.4664146900177, "type": "round"}]}
], 
"result_num": 5}
```
``stats`` may not exist because no analysis results are provided.
The result in ``stats.result`` may not contain attributes, and the ``identity`` may be empty string because the face is not recognized.

### ``Users``

This is mainly for querying the user name according the the identity.

```python
identity = "kai.yu"
try:
    user = Users.objects.get(identity=identity)
    print(user.name)
except Users.DoesNotExist:
    pass

```

### ```Occurences```
Shame that this collection name is a typo...

The occurrences of people.

``identity`` can be "unknown".

Attributes related fields may be empty, but ``location`` and ``img`` always exists.

## Important

PLEASE test with ``main.py`` rather than ``bot.py`` which is for production use, because frequent request of wechat login may cause account locking!!!