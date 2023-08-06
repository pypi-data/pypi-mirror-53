from os import path
from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='peerpkg',
    version='1.3',
    description=long_description,
    long_description=long_description,
    url='https://github.com/ahmedgirach/peer',
    author='Ahmed Girach',
    author_email='ahmed@peerbits.com',
    license='MIT',
    packages=['peerpkg'],
    zip_safe=False
)
