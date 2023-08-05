#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/16 0016 11:04
# @File    : setup.py
# @author  : dfkai
# @Software: PyCharm


from setuptools import setup, find_packages

setup(
    name='Flask_Curd_Db',
    version='1.0.0',
    keywords='flask curd db method',
    description='flask curd db method',
    license='MIT License',
    url='https://github.com/libaibuaidufu/Flask-Curd-Db.git',
    author='libaibuaidufu',
    author_email='libaibuaidufu@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=["sqlalchemy"],
)

"""
python setup.py sdist bdist_wheel 
twine upload dist/*
# or python setup.py sdist bdist_wheel upload
"""
