"""Integrates dogpile.cache for Pyramid
"""
from setuptools import setup, find_packages
import glob
import os.path


def project_path(*names):
    return os.path.join(os.path.dirname(__file__), *names)


setup(
    name='pyramid_dogpile_cache2',
    version='1.0.1',

    install_requires=[
        'Beaker',  # For parsing pylibmc behaviors from ini file.
        'dogpile.cache',
        'pyramid_dogpile_cache',  # For ini file parsing helpers.
        'setuptools',
    ],

    author='Zeit Online',
    author_email='zon-backend@zeit.de',
    license='BSD',
    url='https://github.com/zeitonline/pyramid_dogpile_cache2',

    keywords='pyramid dogpile.cache',
    classifiers="""\
    Environment :: Plugins
    Framework :: Pyramid
    Framework :: Paste
    Intended Audience :: Developers
    License :: OSI Approved :: BSD License
    Programming Language :: Python
    Programming Language :: Python :: 2
    Programming Language :: Python :: 2.7
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3.4
    """.split('\n')[:-1],
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
