# -*- coding: utf-8 -*-
"""Project setup configuration for setuptools"""

from glob import glob

from setuptools import find_packages
from setuptools import setup

setup(
    name='sphinx_vcs_changelog',
    description='Project Git Changelog for Sphinx',
    version='0.1.1',
    author='Aleksey Marin',
    author_email='asmadews@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[
        path.splitext(path.basename(path))[0] for path in glob('src/*.py')
    ],
    include_package_data=True,
    zip_safe=False,
    data_files=[],
    entry_points={
        "console_scripts": [
            "vcs_changelog=sphinx_vcs_changelog.cmdline:main",
        ]
    },
    tests_require=["pytest"],
    install_requires=[
        'six',
        'sphinx',
        'GitPython>=0.3.6',
        'setuptools >= 36.0.1'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Environment :: Plugins',
        'Framework :: Sphinx',
        'Framework :: Sphinx :: Extension',
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Natural Language :: Russian',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    long_description_content_type='text/x-rst',
    long_description="""
    sphinx-vcs-changelog is an extension to the Sphinx documentation tool
    supporting git history excerpt includes into your documentation.
    Useful in cases of preparing release changelog or describe specific changes
    in documentation.
    """
)
