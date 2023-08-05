import os
from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hwp-py',
    version='0.0.1',
    descriptin='HWP Library for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Hanjun Kim',
    author_email='hallazzang@gmail.com',
    python_requires='>=3.6.0',
    url='https://github.com/hallazzang/hwp-py',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ])