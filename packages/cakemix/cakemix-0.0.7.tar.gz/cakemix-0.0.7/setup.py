import setuptools
import os

with open(os.path.join(os.getcwd(), "README.md"), "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cakemix",
    version="0.0.7",
    author="Mesut Varlioglu, PhD",
    author_email="varlioglu@gmail.com",
    description="Python library to open Office documents, automate the data analysis and making presentations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/varlmes/cakemix",
    packages=setuptools.find_packages(),
    install_requires=[
        "bs4",
        "matplotlib",
        "numpy",
        "xlrd",
		"flask"
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False
)
