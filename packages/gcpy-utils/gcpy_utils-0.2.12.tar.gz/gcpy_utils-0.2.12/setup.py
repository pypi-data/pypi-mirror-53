# coding:utf-8
__author__ = 'qinman'
# create by qinman on 2018/4/13

from setuptools import setup, find_packages

setup(
    name='gcpy_utils',
    version='0.2.12',
    description=(
        '<公用函数的封装>'
    ),
    author='zhoukunpeng',
    author_email='zhoukunpeng504@163.com',
    packages=find_packages(),
    install_requires=['happybase', 'happybase-monkey', 'gevent==1.2.2', 'redis', 'django==1.4.22',
                      "threadspider==0.3.4",
                      "celery==4.1.0"]
)
