from setuptools import setup

setup(name='util',
      description='General utilities for PaKeT project',
      version='1.0.0',
      url='https://github.com/paket-core/util',
      license='GNU GPL',
      packages=['util'],
      install_requires=[
          'coloredlogs==10.0',
      ],
      test_suite='tests',
      zip_safe=False)
