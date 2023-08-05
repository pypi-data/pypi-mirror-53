import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="ninehundred-basetoascii",
    version="0.0.10",
    description="Converts input from binary, hex, or oct to readable text",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ninehundred/basetoascii",
    author="Daniel O'Dowd",
    author_email="ninehundred@hotmail.co.uk",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["basetoascii"],
    include_package_data=True,
    install_requires=[""],
    entry_points={
        "console_scripts": [
            "basetoascii=reader.__main__:main",
        ]
    },
)
