#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='nfc_module',
    version=1,
    description=(
        'NFC读写操作'
    ),
    long_description='为NFC读卡器设备制作的便于操作的软件，样例：\nstart()\n\
wakeUp()\n\
uid = getUid()\n\
checkKey(uid, [])\n\
writeBar(5, [1, 9, 9, 8, 1, 1, 2, 3])\n\
print(\'5s: \' + str(readBar(5)))',
    author='cpak00',
    author_email='cymcpak00@gmail.com',
    maintainer='cpak00',
    maintainer_email='cymcpak00@gmail.com',
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    url='https://www.github.com/cpak00/nfc_module',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'pyserial==3.4',
    ],
)
