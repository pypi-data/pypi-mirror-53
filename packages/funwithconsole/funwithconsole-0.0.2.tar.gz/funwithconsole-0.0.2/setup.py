import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="funwithconsole",
    version="0.0.2",
    author="Can Kurt",
    author_email="can.kurt.aa@gmail.com",
    description="funny console tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cccaaannn/funwithconsole",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)