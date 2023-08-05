# DeepSegment: A sentence segmenter that actually works!
Note: For the original implementation please use the "master" branch of this repo.

This implementation is trained on data from various sources. (v1 or the model in master branch is trained only on Tatoeba data).

The Demo is available at http://bpraneeth.com/projects

# Installation:
```
pip install --upgrade deepsegment
# please install tensorflow or tensorflow-gpu separately. Tested with tf and tf-gpu versions 1.8 to 2.0
```

# Supported languages:
en - english (Trained on data from various sources)

fr - french (Only Tatoeba data)

it - italian (Only Tatoeba data)


# Usage:

```
from deepsegment import DeepSegment
# The default language is 'en'
segmenter = DeepSegment('en')
segmenter.segment('I am Batman i live in gotham')
# ['I am Batman', 'i live in gotham']

```

Training deepsegment on custom data: https://colab.research.google.com/drive/1CjYbdbDHX1UmIyvn7nDW2ClQPnnNeA_m

# To Do:
2. Publish docker tf-serving image and deepsegment-client.
