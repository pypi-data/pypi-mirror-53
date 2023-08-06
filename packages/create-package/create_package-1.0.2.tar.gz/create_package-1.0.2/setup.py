import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="create_package",
    version="1.0.2",
    author="Rui Aguiar",
    author_email="raguiar1000@gmail.com",
    description="A package that makes it easy to create Pypi packages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raguiar2/create-python-package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 
