#!/usr/bin/env python

from distutils.core import setup

import sys
sys.path.insert(1, 'src/')
from m2c.version import __version__


setup(name='mail2caldav',
      version=__version__,
      description='Automatically merge mail invitations into a cladav calendar.',
      author='Sven Klomp',
      author_email='mail@klomp.eu',
      url='https://github.com/avanc/mail2caldav',
      packages=['m2c'],
      package_dir={'m2c': 'src/m2c'},
      scripts=['src/bin/mail2caldav'],
      data_files=[('config', ['config/m2c.cfg'])],
      license="GPLv2",
      platforms=["Linux"],
      long_description=""
     )
