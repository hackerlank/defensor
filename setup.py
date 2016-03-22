#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
from os import path 

exec(open('defensor/_version.py').read())

with open('requirements.txt', 'r') as f:
    requires = [x.strip() for x in f if x.strip()]


setup(name='defensor',
      version=__version__,
      author='Wanyuan Yang',
      author_email='yangwanyuan@ztgame.com',
      url="http://gitlab.ztgame.com.cn/scloudm/defensor.git",
      description="MessagePack Defensor for Python",
      long_description=open(
          path.join(
              path.dirname(__file__),
              'README'
          )
      ).read(),
      packages=find_packages(),
      install_requires=requires,
      license="Giant Software License",
      classifiers=[
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: Apache Software License'],
      package_dir = {'defensor': 'defensor'},
      package_data = {'defensor': ['api/templates/*.html']},
      scripts=[
          'bin/defensor-api',
          'bin/defensor-agent',
          ],
      data_files=[('/etc/init.d', ['etc/init.d/scloudm-defensor-api', \
                                   'etc/init.d/scloudm-defensor-agent']),
                  ('/etc/defensor', ['etc/agent.conf.sample', \
                                      'etc/api.conf.sample']),
                  ('/var/log/defensor', []),
                  ('/var/run/defensor', []),
                  ]
      )
