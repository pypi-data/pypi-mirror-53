#!/usr/bin/env python3

from setuptools import setup, find_packages

with open('README.md','r') as fh:
    long_description = fh.read()

setup(
    name ="CryptNinja",
    version = "0.0.0",
    author="Jayant Raizada",
    author_email="jayantraizada1993@live.com",
    description="This is a next gen password safe which uses Key gen algos like argon hash.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages= find_packages(),
    py_modules=['CryptNinja.login'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['cryptography','argon2-cffi','tabulate','pycryptodome'],
    license='MIT',
    entry_points = {
        'console_scripts': ['CryptNinja=CryptNinja.login:main'],
    }
)

