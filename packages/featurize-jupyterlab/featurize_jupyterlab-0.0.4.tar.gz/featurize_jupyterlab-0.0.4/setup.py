"""
Setup Module to setup Python Handlers (Git Handlers) for the Git Plugin.
"""
import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name='featurize_jupyterlab',
    version='0.0.4',
    author='',
    description="A server extension for JupyterLab's featurize extension",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=required
)
