"""Integrates dogpile.cache for Pyramid
"""
from setuptools import setup, find_packages
import glob
import os.path


def project_path(*names):
    return os.path.join(os.path.dirname(__file__), *names)


setup(
    name='pyramid_dogpile_cache2',
    version='1.0.dev0',

    install_requires=[
        'setuptools',
    ],

    extras_require={
        'test': [
        ],
    },

    author='Zeit Online',
    author_email='zon-backend@zeit.de',
    license='BSD',
    url='https://github.com/zeitonline/pyramid_dogpile_cache2',

    keywords='',
    description=__doc__.strip(),
    long_description='\n\n'.join(open(project_path(name)).read() for name in (
        'README.rst',
        'HACKING.rst',
        'CHANGES.txt',
    )),

    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    data_files=[('', glob.glob(project_path('*.txt')))],
    zip_safe=False,
)
