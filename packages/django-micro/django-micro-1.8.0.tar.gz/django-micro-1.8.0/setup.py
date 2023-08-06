import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding='utf8').read()

setup(
    name='django-micro',
    description='Django as a microframework',
    long_description=read('README.rst'),
    keywords='django microframework',
    py_modules=['django_micro'],
    version='1.8.0',
    author='Max Poletaev',
    author_email='max.poletaev@gmail.com',
    url='https://github.com/zenwalker/django-micro',
    license='BSD',
    install_requires=[
        'django>=2.1',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
    ],
)
