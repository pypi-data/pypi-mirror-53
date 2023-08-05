# -*- coding: utf-8 -*- 
"""
@User     : Frank
@File     : setup.py
@DateTime : 2019-09-16 11:24 
@Email    : frank.chang@lexisnexis.com
"""
from setuptools import setup,find_packages
import io
import re

with io.open('README.rst', 'r', encoding='utf8') as f:
    long_description = f.read()

with io.open("src/useful_decoration/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)


setup(
    name="useful_decoration",
    license='Apache License 2.0',
    version=version,
    packages=find_packages("src"),
    zip_safe=False,
    include_package_data=True,
    package_dir={"": "src"},
    long_description=long_description,
    url='https://github.com/changyubiao/useful_decoration',
    author='frank',
    author_email='frank.chang@lexisnexis.com',
    description='powerful and useful decorations',

    project_urls={
        "Documentation": "https://useful-decoration.readthedocs.io/en/latest/",
        "Code": "https://github.com/changyubiao/useful_decoration",
    },

    python_requires='>=3.6',
    install_requires=[
        "loguru>=0.3.2",

    ],

)

