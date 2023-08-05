"""
Setup for Docs Configuration
"""
from setuptools import setup, find_packages


with open('requirements.txt') as f:
    install_reqs = f.read().splitlines()


setup(
    setup_requires=['pbr'],
    pbr=True,
    install_requires=install_reqs
)
