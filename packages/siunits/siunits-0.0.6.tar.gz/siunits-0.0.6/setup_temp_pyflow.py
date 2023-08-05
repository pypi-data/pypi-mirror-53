import setuptools
 
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="siunits",
    version="0.0.6",
    author="David O'Connor",
    author_email="david.alan.oconnor@gmail.com",
    license="MIT",
    description="Perform operations on SI units",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/David-OConnor/si_units",
    packages=setuptools.find_packages(),
    keywords=" si units dimensional analysis",
    classifiers=[
    "Programming Language :: Python :: 3 :: Only",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Topic :: Scientific/Engineering",
],
    python_requires=">=3.7",
)
