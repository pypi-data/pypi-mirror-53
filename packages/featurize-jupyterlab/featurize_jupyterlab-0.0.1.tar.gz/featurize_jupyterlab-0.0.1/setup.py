"""
Setup Module to setup Python Handlers (Git Handlers) for the Git Plugin.
"""
import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')) as f:
    install_requires = f.read().splitlines()

setuptools.setup(
    name='featurize_jupyterlab',
    version='0.0.1',
    author='',
    description="A server extension for JupyterLab's featurize extension",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    package_data={'featurize_jupyterlab': ['*']},
)
