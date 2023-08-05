import setuptools


with open("README.md", "r") as fh:
    long = fh.read()

setuptools.setup(
    # Project information
    name="powerball",
    version="0.2.1",
    author="Matthew Marshall",
    author_email="matthewmarshall124@gmail.com",
    url="https://github.com/mmarshall124/powerball",
    license="MIT",

    # Description
    description="A tool for competitive lottery analysis of bacterial groups.",
    long_description=long,
    long_description_content_type="text/markdown",
    # Packages
    packages=setuptools.find_packages(),
    # Classifiers
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],



)