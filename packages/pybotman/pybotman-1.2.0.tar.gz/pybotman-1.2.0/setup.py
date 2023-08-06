from os import path

from setuptools import setup

version = "1.2.0"

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.MD'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pybotman',
    version=version,
    description='Python API wrapper for botman bots',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Flowelcat/pybotman',
    download_url='https://github.com/Flowelcat/pybotman/archive/v.{}.tar.gz'.format(version),
    author='Flowelcat',
    author_email='flowelcat@gmail.com',
    keywords=["botman", 'pybotman', 'botmanbot', 'botmanapi'],
    license='apache-2.0',
    install_requires=['requests', 'python-dateutil'],
    tests_require=['httmock'],
    packages=['pybotman'],
    python_requires='>=3.5.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
