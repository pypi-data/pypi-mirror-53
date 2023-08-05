#!/usr/bin/env python3
from setuptools import setup, find_packages


def read_requirements(filename):
    return [req.strip() for req in open(filename)]


requirements = read_requirements('requirements.txt')
dev_requirements = read_requirements('requirements-dev.txt')

setup(
    name='madeleine',
    version=open('VERSION').read().strip(),
    author='Lucidiot',
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"],
    ),
    package_data={
        '': ['*.md', 'LICENSE', 'README'],
    },
    python_requires='>=3.5',
    install_requires=requirements,
    extras_require={
        'dev': dev_requirements,
        'yaml': ['pyyaml>=5.1'],
        'toml': ['toml>=0.10'],
    },
    tests_require=dev_requirements,
    test_suite='tests',
    license='GNU General Public License 3',
    description="Configurable random text generation",
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    keywords="random text generation",
    url="https://gitlab.com/Lucidiot/madeleine",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    project_urls={
        "Source Code": "https://gitlab.com/Lucidiot/madeleine",
        "Bug Tracker": "https://gitlab.com/Lucidiot/madeleine/issues",
        "GitHub Mirror": "https://github.com/Lucidiot/madeleine",
    }
)
