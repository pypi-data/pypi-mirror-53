import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyzedis',
    version='0.0.001',
    author="David Holtz",
    author_email="david.richard.holtz@gmail.com",
    description="A Python client for zedis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/drbh/pyzedis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
    ],
)
