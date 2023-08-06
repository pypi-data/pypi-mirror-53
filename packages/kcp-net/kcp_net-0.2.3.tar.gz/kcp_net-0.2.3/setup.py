# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="kcp_net",
    version='0.2.3',
    zip_safe=False,
    platforms='any',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    install_requires=['gevent', 'events', 'kcp_wrapper'],
    url="https://github.com/dantezhu/kcp_net",
    license="MIT",
    author="dantezhu",
    author_email="zny2008@gmail.com",
    description="kcp_net",
)
