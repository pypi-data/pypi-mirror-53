#!/usr/bin/env python3
from setuptools import setup, find_packages
from typing import List


def read_requirements(filename: str) -> List[str]:
    return [req.strip() for req in open(filename)]


# requirements = read_requirements('requirements.txt')
requirements: List[str] = []
dev_requirements = read_requirements('requirements-dev.txt')

setup(
    name='objtools',
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
    },
    tests_require=dev_requirements,
    test_suite='tests',
    license='GNU General Public License 3',
    description="Miscellaneous helpers for objects.",
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    keywords="object tools utils utilities",
    url="https://gitlab.com/Lucidiot/objtools",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    project_urls={
        "Source Code": "https://gitlab.com/Lucidiot/objtools",
        "Bug Tracker": "https://gitlab.com/Lucidiot/objtools/issues",
        "GitHub Mirror": "https://github.com/Lucidiot/objtools",
    }
)
