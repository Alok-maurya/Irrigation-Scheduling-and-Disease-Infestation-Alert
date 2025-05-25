# -*- coding: utf-8 -*-
"""
Created on Sat May 24 23:29:17 2025

@author: ALOK KUMAR
"""

from setuptools import setup, find_packages

setup(
    name="Alert",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "openpyxl"  # for reading Excel files
    ],
    author="Alok Kumar Maurya",
    author_email="akmaurya.iitkgp@gmail.com",
    description="Irrigation scheduling and disease infestation alert GUI",
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
