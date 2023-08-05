import pathlib
from setuptools import setup,find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="pysmz3",
    version="1.0.1",
    author="Thomas Prescott",
    author_email="tcprescott@gmail.com",
    description="A python module for interacting with samus.link, such as generating new smz3 games and retrieving old games.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tcprescott/python-pysmz3",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
    ],
    install_requires=['aiohttp'],
)