from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dsalg',
    version='0.0.1',
    description="It's a library of Data Structures in Python.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/get-dataxy/dsalg',
    author='Kiran Kumar Kotari',
    author_email='kirankotari@live.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='data structures in python ds algorithms',
    packages=find_packages(exclude=['tests', 'data', 'asserts']),
)
