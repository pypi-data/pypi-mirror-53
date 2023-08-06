import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mealgenerator-Rhyknowscerious",
    version="2019.09.29.7",
    author="Ryan James Decker",
    author_email="email@iamryanjdecker.com",
    description="Generates random meals for meal planning.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/Rhyknowscerious/mealgenerator.py/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=2.7,<3.0',
)

