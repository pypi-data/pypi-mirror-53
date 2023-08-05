from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.txt'), encoding='utf-8') as f:
   long_description = f.read()


setup(name='ms_querytool',
      version='1.2',
      description='Tool to ingest a SQL txt file, run all of the statements, and return the results',
      author='Marc Stumbo',
      author_email='marc.stumbo@verizonwireless.com',
      license='MS',
      py_modules=['ms_querytool'],
      #install_requires=['os', 'sys', 'pyodbc', 'pandas', 'logging', 'datetime'],
      python_requires='>3'
    )
