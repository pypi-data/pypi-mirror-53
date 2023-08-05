"""
Setup Module to setup Python Handlers (Git Handlers) for the Git Plugin.
"""
import setuptools
import os

install_requires = []
requirement_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'requirements.txt')
if os.path.isfile(requirement_file):
    with open(requirement_file) as f:
        install_requires = f.read().splitlines()

setuptools.setup(
    name='featurize_jupyterlab',
    version='0.0.3',
    author='',
    description="A server extension for JupyterLab's featurize extension",
    long_description="",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    package_data={'featurize_jupyterlab': ['*']},
)
