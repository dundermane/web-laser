#!/usr/bin/env python

from distutils.core import setup

install_requires = [
    'Flask >= 0.10.0',
    'datetime'   
]

setup(name='laser-interlock',
      version='0.1',
      description='Laser Web UI',
      author='Matt Ewing',
      author_email='mewing6732@gmail.com',
      url='laser.interlockroc.com',
      packages=['ui', 'sender'],
      include_package_data=True,
      zip_safe=False,
      install_requires = install_requires,
     )
