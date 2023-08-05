from setuptools import setup

setup(
    name='context-helpers',
    version='0.1.4',
    description='Helpers for dealing with context managers',
    url='https://github.com/firba1/context-helpers',
    author='Ben Bariteau',
    author_email='ben.bariteau@gmail.com',
    license='MIT',
    install_requires=[
        'contextlib2',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['context_helpers'],
)
