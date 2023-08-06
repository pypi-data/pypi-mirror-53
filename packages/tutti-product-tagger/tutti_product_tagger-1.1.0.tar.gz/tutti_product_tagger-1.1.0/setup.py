""" 
See [1] on how to write proper `setup.py` script.
[1] https://github.com/pypa/sampleproject/blob/master/setup.py
"""
from setuptools import setup, find_packages
from tutti_product_tagger import __version__

setup(
    name='tutti_product_tagger',
    version=__version__,
    description='A tutti.ch automatic product tagger.',
    long_description='Very simple logic to tag furniture products from Swiss-German text ads.',
    author='Oscar Saleta',
    author_email='oscar@tutti.ch',
    license='Proprietary',
    keywords=['product', 'tagging'],
    packages=find_packages(exclude=['contrib', 'docs', '*test*']),
    python_requires='>=3.5.2',
    install_requires=[
        'pandas',
        'fuzzywuzzy',
        'python-Levenshtein'
    ],
    zip_safe=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
    include_package_data=False
)
