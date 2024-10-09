from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="gemini",
    version="0.1.0",
    description="Back-end for GEMINI GWAS",
    author="Pranav Ghate",
    author_email="pghate@ucdavis.edu",
    install_requires=required,
    packages=find_packages(),
    include_package_data=True
)