import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="bin_packing_problem",
    version="1.0.0",
    author="ibigpapa",
    author_email="issues@github.url",
    description="Provides 1D bin packing logic.",
    license="MIT",
    keywords="1D Bin Packing FirstFit NextFit BestFit FFD",
    url="https://github.com/ibigpapa/bin_packing_problem",
    packages=['binpackp'],
    package_data={'': ['LICENSE']},
    include_package_data=True,
    long_description=read("README"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries"
    ]
)
