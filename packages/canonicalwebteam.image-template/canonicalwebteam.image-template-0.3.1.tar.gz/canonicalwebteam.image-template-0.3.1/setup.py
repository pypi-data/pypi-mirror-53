#! /usr/bin/env python3

# Core
from setuptools import setup

setup(
    name="canonicalwebteam.image-template",
    version="0.3.1",
    author="Canonical webteam",
    author_email="webteam@canonical.com",
    url="https://github.com/canonical-web-and-design/canonicalwebteam.image-template",
    packages=["canonicalwebteam", "canonicalwebteam.image_template"],
    include_package_data=True,
    description=("Generate <img> markup block for an image."),
    long_description=open("README.rst").read(),
    install_requires=["jinja2>=2"],
    test_suite="tests",
)
