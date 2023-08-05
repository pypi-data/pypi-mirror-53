"""
Setup Module to setup Python Handlers (Git Handlers) for the Git Plugin.
"""
import os
import setuptools

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')) as f:
    install_requires = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='featurize_runtime',
    version='0.0.1',
    author='',
    description="Featurize runtime",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    package_data={'featurize_runtime': ['*']},
)
