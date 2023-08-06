import os
import setuptools


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


__name__ = "spriteutilkangkang"
__version__ = "1.0.0"
__author__ = "Khang TRAN"
__author_email__ = "haphong12@gmail.com"
__copyright__ = "Copyright (C) 2019, Intek Institute"
__credits__ = "Intek Institute"
__maintainer__ = "Khang TRAN"
__url__ = "https://github.com/haphongpk12/Sprite-Sheet"

setuptools.setup(
    name=__name__,
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    copyright=__copyright__,
    credits=__credits__,
    license="MIT",
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    maintainer=__maintainer__,
    url=__url__,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
