"""
Setup Module to setup Python Handlers (Git Handlers) for the Git Plugin.
"""
import os
import setuptools

if os.path.isfile('requirements.txt'):
    with open('requirements.txt') as f:
        install_requires = f.read().splitlines()

if os.path.isfile('README.md'):
    with open("README.md", "r") as fh:
        long_description = fh.read()

setuptools.setup(
    name='featurize_runtime',
    version='0.0.3',
    author='',
    description="Featurize runtime",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    package_data={'featurize_runtime': ['*']},
    include_package_data = True,
    entry_points = {
        'console_scripts': ['featurize=featurize_runtime:cli'],
    }
)
