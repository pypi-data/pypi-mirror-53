import os

from setuptools import setup, find_packages
import smm_utils as app

def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

setup(
  name='smm_utils',
  version=app.__version__,
  description='Utilities for smm guru project',
  long_description=read('README.rst'),
  author='Evgeny Basmov',
  author_email='coykto@gmail.com',
  url='https://gitlab.com/smm-guru/smm-utils',
  license='MIT',
  platforms=['OS Independent'],
  packages=['smm_utils'],
  zip_safe=False,
  classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
)
