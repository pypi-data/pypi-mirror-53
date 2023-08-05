# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name              = 'stepwisereg',
    packages          = ['stepwisereg'],
    version           = '0.1.0',
    description       = 'Stepwise Regression in Python',
    long_description  = 'Forward Stepwise Regression in Python like R using AIC',
    author = 'Avinash Barnwal',
    author_email = 'avinashbarnwal123@gmail.com',
    url = 'https://github.com/avinashbarnwal/stepwisereg',
    maintainer='Avinash Barnwal',
    maintainer_email='avinashbarnwal123@gmail.com',
    install_requires=[
    'numpy',
    'pandas',
	'statsmodel',
	'functools',
	're'
    ],
    download_url = 'https://github.com/avinashbarnwal/stepwisereg/archive/0.1.0.tar.gz',
    keywords = ['stepwise', 'python3', 'sklearn','regression'],
    license='The MIT License (MIT)',
    classifiers = ["Programming Language :: Python :: 3",
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",],
)
