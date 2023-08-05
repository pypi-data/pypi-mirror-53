from pathlib import Path
from setuptools import setup, find_packages

setup(
    name='runt',
    version='0.0.2',
    url='https://github.com/clayboone/runt.git',
    author='Clay Boone',
    author_email='tener.hades@gmail.com',
    description='A job-managing task runner',
    long_description=Path('README.rst').read_text(),
    packages=find_packages(),
)
