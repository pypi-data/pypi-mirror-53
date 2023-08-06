#!/usr/bin/env python3
import os
from setuptools import setup

if __name__ == '__main__':
    os.chdir(
        os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
    with open('README.md', 'r') as fh:
        long_description = fh.read()
    setup(
        name='django-storage-webdav',
        version='0.1.2',
        description='Django Storage System for WebDAV',
        author='A. Palsson',
        author_email='contact@apalsson.info',
        url='https://gitlab.com/apalsson/django-webdav-storage',
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=['django_storage_webdav', ],
        install_requires=[
            'django>=2.2', 'lxml', 'python-dateutil', 'requests'],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Framework :: Django :: 2.2',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
        ],
        python_requires='>=3.5',
    )
