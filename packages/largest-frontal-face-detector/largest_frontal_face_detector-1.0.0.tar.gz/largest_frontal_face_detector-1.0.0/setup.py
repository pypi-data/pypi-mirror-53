import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="largest_frontal_face_detector",
    version="1.0.0",
    author="Devang Kulshreshtha",
    author_email="devang.kulshreshtha.cse14@itbhu.ac.in",
    description="Python pakage for detecting largest face in an image",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/devangkulshreshtha/largest_face_detector",
    install_requires=[
          'numpy',
          'dlib',
          'pillow'
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)