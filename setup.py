import setuptools
import os


def get_description():
    if os.path.isfile("README.md"):
        with open("README.md", "r") as fh:
            desc = fh.read()
    else:
        desc = ""
    return desc


setuptools.setup(
    name="flexmod",
    version="0.1.2",
    description="A module for other modules to allow flexible (yet not error-prone) configuration.",
    long_description=get_description(),
    long_description_content_type="text/markdown",
    author="Haochuan Wei",
    author_email="pepsimixt@gmail.com",
    url="https://github.com/haochuanwei/flexmod",
    packages=setuptools.find_packages(include=["flexmod*"]),
    install_requires=[
    ],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
