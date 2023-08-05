import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pylates",
    version="0.0.3",
    author="Marco S. Nobile",
    author_email="marco.nobile@unimib.it",
    description="Dilation Functions in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aresio/pylates",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)