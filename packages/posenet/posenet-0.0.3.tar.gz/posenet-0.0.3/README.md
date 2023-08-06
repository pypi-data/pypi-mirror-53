# Posenet

An easy to use implementation of the Posenet neural network. Packaged from [@rwrightman's posenet model](https://github.com/rwightman/posenet-python).

## Installation

To install, one can run:

```
pip install yale-dhlab-posenet
```

## Usage

This module is designed for one of two uses. The first use case is when one has a directory of images and wants to predict poses for each image in that directory. To do so, one can run:

```python
from posenet import process_images

process_images({
  'image_dir': 'path-to/images/',
  'output_dir': 'output',
})
```

This will process each image in the specified directory and will save the resulting data structures to `./output`.

Each input image will have two corresponding outputs in `./output`: a `.jpg` file with identified keypoints displayed, and a `.npy` file with identified keypoints stored in a numpy format. The former looks like this:

![img output preview](./assets/images/sample-output?raw=true)

The `.npy` file contains data in the following format:

```bash


```