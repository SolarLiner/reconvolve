from setuptools import setup
from lib import __version__

setup(
    name="reconvolve",
    version=__version__,
    author="Solarliner",
    author_email="solarliner@gmail.com",
    description="Convolution IR creation through recording sine sweep response",
    long_description=open("README.md").read(),
    url="https://github.com/SolarLiner/reconvolve",
    classifiers=[
        "Programming Language :: Python 3.7",
        "Development Planning :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Scientific/Engineering",
        "Typing :: Typed"
    ]
)
