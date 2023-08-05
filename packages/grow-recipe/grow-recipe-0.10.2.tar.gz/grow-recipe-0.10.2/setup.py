#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='grow-recipe',
    version='0.10.2',
    author='Jason Biegel',
    url='https://github.com/njason/grow-recipe-python',
    license='LICENSE',
    description='Store plant grow recipes in a structured XML format',
    packages=find_packages(exclude=['docs', 'samples', 'tests']),
    package_data={'grow_recipe': ['grow-recipe.xsd']}
)
