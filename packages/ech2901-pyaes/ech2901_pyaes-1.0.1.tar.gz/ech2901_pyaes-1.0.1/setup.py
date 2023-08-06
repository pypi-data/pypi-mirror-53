from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()


setup(
    name='ech2901_pyaes',
    version='1.0.1',
    packages=find_packages(),
    python_requires='>=3.7',

    author='Ellis Harlan',
    author_email='EllisCHarlan@gmail.com',
    description='Python implementatoin of the AES Encryption Algorithm',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ech2901/pyaes',
    liscense='GPL-3.0',



    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers'
    ]




)
