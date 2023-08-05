"""
setup script with information about the project needed when packaged and uploaded to Pypi
"""
import setuptools

with open("VERSION", "r") as fh:
    VERSION = fh.read().strip()

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="mark-python-client",
    version=VERSION,
    author="Georgi Nikolov",
    author_email="contact@cylab.be",
    description="A client library for MARK server",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://gitlab.cylab.be/cylab/mark-python-client",
    packages=setuptools.find_packages(exclude=("tests")),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
