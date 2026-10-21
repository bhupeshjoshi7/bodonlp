# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

long_desc = ""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as fh:
        long_desc = fh.read()

setup(
    name="bodonlp",
    version="1.0.0",
    author="Bhupesh Joshi",
    author_email="bhupeshjoshi@example.com",
    maintainer="Bhupesh Joshi",
    maintainer_email="bhupeshjoshi@example.com",
    description="Bodo (बड़ो / बर') Language Standard NLP Library: 36,000+ Dictionary Entries, Universal Translation, Classifier Engine, and Cultural Heritage",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/bhupeshjoshi7/bodo",
    project_urls={
        "Documentation": "https://github.com/bhupeshjoshi7/bodo/blob/main/DOCUMENTATION.md",
        "Source": "https://github.com/bhupeshjoshi7/bodo",
        "Bug Tracker": "https://github.com/bhupeshjoshi7/bodo/issues",
    },
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "bodonlp.lexicon": ["data/*.json"],
    },
    entry_points={
        "console_scripts": [
            "bodonlp = bodonlp.cli:main",
            "bodo-cli = bodonlp.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",
        "Natural Language :: Bodo",
    ],
    python_requires=">=3.8",
)
