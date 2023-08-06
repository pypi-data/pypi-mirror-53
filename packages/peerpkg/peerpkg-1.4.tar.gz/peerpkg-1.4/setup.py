from setuptools import setup

LONG_DESCRIPTION = open("README.md").read()

setup(
    name='peerpkg',
    version='1.4',
    description=LONG_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url='https://github.com/ahmedgirach/peer',
    author='Ahmed Girach',
    author_email='ahmed@peerbits.com',
    license='MIT',
    packages=['peerpkg'],
    zip_safe=False
)
