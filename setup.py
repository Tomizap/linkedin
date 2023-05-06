from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = "0.0.1"
DESCRIPTION = ""

setup(
    name="indeed",
    version=VERSION,
    author="TZ",
    author_email="<zaptom@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['selenium', 'webdriver_manager'],
    keywords=[],
    classifiers=[]
)
