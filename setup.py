from setuptools import setup

setup(name='logger',
      description='Logger for PaKeT project',
      version='1.0.0',
      url='https://github.com/paket-core/logger',
      license='GNU GPL',
      packages=['logger'],
      install_requires=[
          'coloredlogs==9.3.1',
      ],
      test_suite='tests',
      zip_safe=False)
