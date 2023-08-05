import os
import sys
import warnings

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))


with open('LONG_DESCRIPTION.rst') as f:
    long_description = f.read()

version_contents = {}
with open(os.path.join('verifai_sdk', 'version.py')) as f:
    exec(f.read(), version_contents)

setup(
    name='verifai_sdk',
    version=version_contents['VERSION'],
    description='Python SDK for Verifai',
    long_description=long_description,
    author='Verifai',
    author_email='support@verifai.com',
    url='https://github.com/verifai-id-verification/verifai-sdk-python',
    license='Apache Software License',
    packages=['verifai_sdk', ],
    #package_data={'verifai_sdk': ['path/to/data']},
    install_requires=[
        'requests >= 2.0.0',
        'Pillow >= 3.0.0'
    ],
    #test_suite='tests',
    #tests_require=['unittest2', 'mock'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ])