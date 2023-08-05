# Copyright 2019 The RE2 Authors.  All Rights Reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import setuptools

ext = setuptools.Extension(
    name='_re2',
    sources=['_re2.cc'],
    libraries=['re2'],
    extra_compile_args=['-fvisibility=hidden'],
)

setuptools.setup(
    name='google-re2',
    version='0.0.0',
    description='RE2 Python bindings',
    url='https://github.com/google/re2',
    author='The RE2 Authors',
    author_email='re2-dev@googlegroups.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: C++',
        'Programming Language :: Python :: 3.6',
    ],
    ext_modules=[ext],
    py_modules=['re2'],
    python_requires='~=3.6',
    install_requires=['six'],
)
