from setuptools import setup, find_packages

import os
from runpy import run_path

d = run_path(os.path.join('awkupy', '_version.py'))
__version__ = d['__version__']

setup(
    name='awkupy',
    url='https://github.com/jadelord/awkupy',
    download_url='https://github.com/jadelord/awkupy',
    version=__version__,
    description='A simple Python interface for running AWK natively',
    license='GPL',
    platforms=['any'],
    author='Ashwin Vishnu',
    author_email='avmo@kth.se',
    packages=find_packages(exclude=['doc', 'tests']),
    entry_points={
        "console_scripts": "iawk=iawk.__main__:main",
    }
)
