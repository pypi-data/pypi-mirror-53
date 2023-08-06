#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='shangyu_pypi',  # How you named your package folder (MyLib)
    version='0.0.1',  # Start with a small number and increase it with every change you make
    author='ShangYu Chiang',  # Type in your name
    author_email='d07945011@ntu.edu.tw',   # Type in your E-Mail
    url='',  # Provide either the link to your github or to your website
    description=u'Test_Yu',  # description - Give a short description about your library
    packages=['shangyu_pypi'],  # packages - Chose the same as "name"
    install_requires=[],
    python_requires='==2.7.*',
    entry_points={
        'console_scripts': [
            'ShangYu=shangyu_pypi:ShangYu',
            'test2019=shangyu_pypi:test2019',
            'shelly=shangyu_pypi:shelly',
        ],
    }
)
