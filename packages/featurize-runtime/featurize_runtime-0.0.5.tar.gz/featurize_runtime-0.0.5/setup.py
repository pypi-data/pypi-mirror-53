"""
Setup Module to setup Python Handlers (Git Handlers) for the Git Plugin.
"""
import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()


setuptools.setup(
    name='featurize_runtime',
    version='0.0.5',
    author='',
    description="Featurize runtime",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=required,
    include_package_data = True,
    entry_points = {
        'console_scripts': ['featurize=featurize_runtime:cli'],
    }
)
