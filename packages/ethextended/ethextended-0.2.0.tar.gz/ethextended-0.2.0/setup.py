from setuptools import setup

with open("requirements.txt", "r") as file:
    requirements = file.read().split("\n")

with open("README.rst", "r") as file:
    readme = file.read()

setup(
    name='ethextended',
    version='0.2.0',
    packages=['ethextended'],
    url='https://github.com/AlexSSD7/ethextended',
    license='GNU GPL v3',
    author='AlexSSD7',
    author_email='',
    description='Library with extra tools for ethereum, provided by Etherscan, Eth Gas Station, etc.',
    long_description=readme,
    install_requires=requirements
)
