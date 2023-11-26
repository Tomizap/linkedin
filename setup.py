from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

DESCRIPTION = """
Simple Python Package
"""

setup(
    name="linkedin",
    version="0.0.1",
    author="TZ",
    author_email="zaptom.pro@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "pymongo",
        "selenium", 
        "tzmongo @ git+https://github.com/Tomizap/tzmongo.git#egg=tzmongo",
        "selenium_driver @ git+https://github.com/Tomizap/selenium_driver.git#egg=selenium_driver",
        "selenium_sequence @ git+https://github.com/Tomizap/selenium_sequence.git#egg=selenium_sequence"
    ],
    dependency_link=[],
    keywords=[],
    classifiers=[]
)