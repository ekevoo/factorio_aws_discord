#!/usr/bin/env python3

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'boto3',
    'discord.py',
    'PyYAML',
]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author='Ekevoo',
    author_email='x@ekevoo.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: System Administrators',
        'Topic :: Communications :: Chat',
        'Topic :: Games/Entertainment :: Simulation',
        'Topic :: System',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description='FAD is a Discord bot that manages Factorio servers on AWS.',
    install_requires=requirements,
    license='MIT license',
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='factorio aws discord',
    name='factorio_aws_discord',
    packages=find_packages(include=['factorio_aws_discord']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ekevoo/factorio_aws_discord',
    version='0.1.0',
    zip_safe=False,
)
