#! /usr/bin/env python3

from distutils.core import setup

with open('README.md', 'r') as file:
    long_description = file.read()

setup(name='AsyncTcpProxy',
      version='0.4.0',
      description='A proxy handles data to/from a TCP server.',
      long_description=long_description,
      author='Eric Tang',
      author_email='tangcongyuan@gmail.com',
      url='',
      packages=[
          'async_tcp_proxy',
          'async_tcp_proxy.proxy',
          'async_tcp_proxy.server',
      ],
     )

