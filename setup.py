#!/usr/bin/env python

from setuptools import setup

install_requires = [
    'Flask >= 0.10.0',
    'pyformex',
    'datetime' 
]

setup(name='laser-interlock',
      version='0.1',
      description='Laser Web UI',
      author='Matt Ewing',
      author_email='mewing6732@gmail.com',
      url='laser.interlockroc.com',
      packages=['web-laser'],
      install_requires = install_requires,
     )
