"""
Setup Module to setup Python Handlers (Git Handlers) for the Git Plugin.
"""
import setuptools
import os

if os.path.isfile('README.md'):
    with open('README.md', 'r') as fh:
        long_description = fh.read()

if os.path.isfile('requirements.txt'):
    with open('requirements.txt') as f:
        install_requires = f.read().splitlines()

setuptools.setup(
    name='featurize_jupyterlab',
    version='0.0.2',
    author='',
    description="A server extension for JupyterLab's featurize extension",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    package_data={'featurize_jupyterlab': ['*']},
)
