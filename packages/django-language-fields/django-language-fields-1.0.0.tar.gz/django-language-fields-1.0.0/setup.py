import os

from setuptools import setup
import languages as app

def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

setup(
  name='django-language-fields',
  version=app.__version__,
  description='A pluggable django app that provides a comprehensive language and region choices field',
  long_description=read('README.rst'),
  author='Ryan Castner, Evgeny Basmov',
  author_email='ryancastner@gmail.com, coykto@gmail.com',
  url='https://gitlab.com/smm-guru/django-region-language-fields',
  license='MIT',
  platforms=['OS Independent'],
  packages=['languages'],
  zip_safe=False,
  keywords=['django', 'language', 'languages', 'region', 'regions', 'fields'],
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
