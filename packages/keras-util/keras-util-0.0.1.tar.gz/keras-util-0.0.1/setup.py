"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='keras-util',
    version='0.0.1', 
    description='plots training hystory of Keras model',
    long_description=long_description, 
    long_description_content_type='text/markdown',  
    author='Slav Kochepasov', 

    url='https://github.com/smile-on/keras_util', 

    keywords='keras util plot history',
    py_modules=["keras_util"],

    python_requires='>=3',
    install_requires=['matplotlib'],
)
