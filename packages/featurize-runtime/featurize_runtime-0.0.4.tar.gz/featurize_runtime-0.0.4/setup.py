"""
Setup Module to setup Python Handlers (Git Handlers) for the Git Plugin.
"""
import os
import setuptools

install_requires = []
requirement_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'requirements.txt')
if os.path.isfile(requirement_file):
    with open(requirement_file) as f:
        install_requires = f.read().splitlines()

setuptools.setup(
    name='featurize_runtime',
    version='0.0.4',
    author='',
    description="Featurize runtime",
    long_description="",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    package_data={'featurize_runtime': ['*']},
    include_package_data = True,
    entry_points = {
        'console_scripts': ['featurize=featurize_runtime:cli'],
    }
)
