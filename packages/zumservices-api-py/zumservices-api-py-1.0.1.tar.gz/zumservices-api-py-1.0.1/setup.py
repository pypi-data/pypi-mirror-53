import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zumservices-api-py",
    version="1.0.1",
    author="CodingRonin",
    author_email="CodingRonin@zumcoin.org",
    description="Python wrapper to interact with the ZUM Services API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zum-services/zumservices-api-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
    ],
)