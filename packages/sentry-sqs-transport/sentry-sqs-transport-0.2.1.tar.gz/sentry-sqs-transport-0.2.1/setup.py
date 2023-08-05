#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'boto3',
    'sentry-sdk>=0.12.2'
]

setup_requirements = [
    'setuptools_scm>=3.1.0'
]


setup(
    name='sentry-sqs-transport',
    use_scm_version={
        'tag_regex': r'^(?P<prefix>v)?(?P<version>[^\+]+)$'
    },
    description="SQS Transport for the sentry-sdk",
    long_description=readme,
    long_description_content_type='text/x-rst',
    author="Terry Cain",
    author_email='terry@terrys-home.co.uk',
    url='https://github.com/terrycain/sentry-sqs-transport',
    packages=find_packages(include=['sentry-sqs-transport*']),
    include_package_data=True,
    install_requires=requirements,
    license="Apache 2",
    zip_safe=True,
    keywords='sentry sqs',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    setup_requires=setup_requirements,
    python_requires='>=3.6',
)
