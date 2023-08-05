Hyperdimensionality computing machine learning library.

Forked from https://gitlab.com/alehd/hd-lib

# Installation and use

Fork this repository and put it in you projects folder or use pip or pipenv:
```
pip install --user hyperdim
```

If you are using keras or sklearn it will be easy to use hyperdim.
To use a model of dimensionality, say 10000:

```
from hyperdim.hdmodel import HDModel
from hyperdim.utils import to_categorical

import numpy as np

# Dummy datasets
samples = 100
features = 15
classes = 5

x = np.random.random(size = (samples, features))
y = [ int(np.random.random()*classes) for _ in x ]
y = to_categorical(y)

print(x.shape) # (samples, features)
print(y.shape) # (samples, classes)

# Build model
dimensions = 10000
model = HDModel(features, classes, d = dimensions)

# Fit using 30% of the data for validation, using one_shot_fit only
history = model.fit(x, y, validation_split = 0.3, epochs = 1)

print(history.history["acc"])
print(history.history["val_acc"])
```
