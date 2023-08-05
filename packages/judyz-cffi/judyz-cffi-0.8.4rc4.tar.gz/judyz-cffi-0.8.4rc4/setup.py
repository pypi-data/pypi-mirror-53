#!/usr/bin/env python
import io
from setuptools import setup


def read(fname):
    with io.open(fname, encoding="utf8") as fp:
        content = fp.read()
    return content


setup(
    name="judyz-cffi",
    version="0.8.4rc4",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=["judyz_cffi"],
    author="Yves Bastide",
    author_email="yves@botify.com",
    description="Python CFFI Judy wrapper",
    url="https://github.com/botify-labs/judyz",
    setup_requires=["cffi>=1.0.0"],
    cffi_modules=["judyz_cffi/_build.py:ffi"],
    install_requires=["cffi>=1.0.0", "six", "typing"],
    include_package_data=True,
    test_suite="tests",
    tests_require=["nose"],
    license=read("LICENSE"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.7",
    ],
)
