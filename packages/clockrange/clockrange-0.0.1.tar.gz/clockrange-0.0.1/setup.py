# Standard Library Imports
import io
import pathlib
import re

# Third-Party Imports
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()


with io.open("clockrange.py", "rt", encoding="utf8") as f:
    VERSION = re.search(r'__version__ = "(.*?)"', f.read(), re.M).group(1)

setup(
    name="clockrange",
    version=VERSION,
    description="A clock-like periodic sequence generator",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ccortezia/clockrange/",
    author="Cristiano Cortezia",
    author_email="cristiano.cortezia@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=["tests", "tests.*"]),
)
