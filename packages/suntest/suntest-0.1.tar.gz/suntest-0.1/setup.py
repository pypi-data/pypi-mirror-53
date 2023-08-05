from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r",encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name="suntest",
    version = "0.1",
    description='测试',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='sun',
    author_email='syw1894@163.com',
    include_package_data=True,
    url='https://pypi.org/project/suntest',
    packages=find_packages('suntest.py'),
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities'
    ],
)