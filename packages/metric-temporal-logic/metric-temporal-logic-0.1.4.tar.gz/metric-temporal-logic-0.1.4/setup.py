from setuptools import find_packages, setup

setup(
    name='metric-temporal-logic',
    version='0.1.4',
    description='A library for manipulating and evaluating metric temporal logic.',  # noqa
    url='http://github.com/mvcisback/py-metric-temporal-logic',
    author='Marcell Vazquez-Chanlatte',
    author_email='marcell.vc@eecs.berkeley.edu',
    license='MIT',
    install_requires=[
        'funcy',
        'parsimonious',
        'lenses',
        'discrete-signals',
    ],
    packages=find_packages(),
)
