#!usr/bin/env sh

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name="bearnaise-bot",
    author="Helena Strandberg",
    author_email="helena.sisko.strandberg@gmail.com",
    description="Helps you fins a place in Gårda to have lunch.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version="0.1.4",
    py_modules=["find_lunch_in_garda"],
    install_requires=["Click", "requests-html", "fuzzywuzzy", "python-Levenshtein"],
    entry_points="""
        [console_scripts]
        bearnaise-bot=find_lunch_in_garda:find_restaurants
    """,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires=">=3.6",
)
