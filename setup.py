from setuptools import setup

setup(
    name='ORD53',
    version='0.1',
    description='ORD53 python code',
    author='Peter Palfrader',
    author_email='peter@palfrader.org',
    packages=[
        'ORD53',
        'ORD53.common',
        'ORD53.formats',
        'ORD53.graph',
    ],
    scripts=[
        'bin/ord-format'
    ],
    zip_safe=False)
