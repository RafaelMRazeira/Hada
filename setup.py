#!/usr/bin/env python
from setuptools import find_packages, setup


def get_requirements_list(file):
    with open(file, "r", encoding="utf8") as f:
        requirements = [line.replace("\n", "") for line in f.readlines()]
    return requirements


requirements = get_requirements_list("requirements.txt")

setup(
    name="Hada",
    entry_points=dict(console_scripts=["hada=hada.cli:main"]),
    version="0.0.1",
    description="HabeasData Autism open source models",
    author="Rafael Mecheseregian Razeira",
    author_email="rafael.razeira@outlook.com",
    url="https://github.com/RafaelMRazeira/Hada",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "black", "pytest-cov"],
)
