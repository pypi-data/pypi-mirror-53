# /usr/bin/env python
import codecs
import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
    name='djangocms-animate-on-scroll',
    version='1.0.1',
    description='Allows you to add the animate on scroll plugin to a cms page',
    long_description=README,
    long_description_content_type='text/markdown',
    author='michalsnik, Michael Carder',
    license='MIT',
    url='https://github.com/mcldev/djangocms-animate-on-scroll',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'Django>=1.11',
        'django-cms>=3.5',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
