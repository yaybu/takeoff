from setuptools import setup, find_packages
import os

version = '0.0.1.dev0'

setup(
    name='takeoff',
    version=version,
    url="http://yaybu.com/",
    description="Orchestration and configuration management in Python",
    long_description = open("README.rst").read(),
    author="Isotoma Limited",
    author_email="support@isotoma.com",
    license="Apache Software License",
    classifiers = [
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'six',
        'touchdown',
    ],
    entry_points='''
        [console_scripts]
        takeoff = takeoff.main:main
    ''',
)
