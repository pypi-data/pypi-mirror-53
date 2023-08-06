#!/usr/bin/env python
import os

from setuptools import find_packages, setup

# https://packaging.python.org/guides/single-sourcing-package-version/
version = {}
with open(os.path.join("src", "galactica", "__init__.py")) as version_file:
    exec(version_file.read(), version)


with open("README.rst") as readme_file:
    long_description = readme_file.read()

# https://packaging.python.org/guides/distributing-packages-using-setuptools
# http://blog.ionelmc.ro/2014/05/25/python-packaging/
setup(
    name="galactica",
    version=version["__version__"],
    description="Galactic multiphase chemical evolution model",
    author="Juanjo Bazán",
    author_email="hello@juanjobazan.com",
    url="https://github.com/xuanxu/galactica",
    download_url="https://github.com/xuanxu/galactica",
    license="MIT",
    keywords=[
        "galaxies",
        "models",
        "astrophysics",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pyyaml>=5.1",
        "numpy>=1.16",
        "scipy>=1.2",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest_mock",
            "pytest_cov",
        ],
    },
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"": ["sample_input/*"]},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    long_description=long_description,
    include_package_data=True,
    zip_safe=False,
)
