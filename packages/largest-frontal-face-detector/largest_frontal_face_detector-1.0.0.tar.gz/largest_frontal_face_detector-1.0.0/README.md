# Largest Face Detector

The Largest Face Detector is a basic face detector that detects largest frontal face from image using external python dlib library (http://dlib.net/python/index.html).

## Installation

You can install the Largest Face Detector from [PyPI](https://pypi.org/project/largest-frontal-face-detector/1.0.0/):

    pip install largest-frontal-face-detector

The reader is supported on Python 3.6 and above.

## Pre-requisites
    1. numpy (pip install numpy)
    2. dlib (pip install dlib)
    3. PIL (pip install pillow)

NOTE :: These dependency packages will be installed automatically upon installing largest-face-detector package.

## How to use

The Largest Face Detector is a pip package, named `largest_face_detector`.  To detect face in a particular image, call the function `detect_largest_face` with image path as input (relative to current directory you are in)

    >>> import largest_face_detector
    >>> image = largest_face_detector.detect_largest_face('image.jpeg')
    $ Cropped face saved successfully at : /Users/kulshd/2019-10-05T14:08:20.086934_cropped_image.jpeg

The function will return the cropped image as a 2D numpy array and also save it.

Following are some requirements and assumptions for using this package -

    1. Image size must be within [1024,1024]. If it exceeds, NotImplementedError is raised.   
    2. If no face is detected by the package, a warning message is displayed
    3. Currently following image formats are supported - [.jpeg, .jpg, .png]

You can also run test-cases to validate package functionality by downloading source .tar.gz file (https://pypi.org/project/largest-frontal-face-detector/1.0.0/#files) ,extracting and cd into folder largest_frontal_face_detector-1.0.0, and running `python3 -m unittest discover -v`