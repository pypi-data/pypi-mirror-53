

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="infogenomics",
    version="0.5",
    author="Vincenzo Bonnici, Massimiliano Loss",
    author_email="vincenzo.bonnici@univr.it, massimiliano.loss@studenti.univr.it",
    description="Advanced framework for the informational genomics in python3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MassimilianoLoss/Frmw_4_Informational_genomics.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
