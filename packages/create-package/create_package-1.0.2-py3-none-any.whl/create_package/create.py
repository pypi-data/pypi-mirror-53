import os
from pathlib import Path


README_TEXT = """
 ## {}
 This is the starter text for a python package.
"""

SETUP_TEXT = """
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="{}",
    version="1.0.0",
    author="",
    author_email="",
    description="A package that makes it easy to create Pypi packages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 
"""

MIT_LISCENSE = """
MIT License

Copyright (c) [2019] [{}]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

INIT_TEXT = """
name="{}"
__version__ = "1.0.0"
"""

def create_dir():
    package_name = str(input("Please enter the name of your package: "))
    package_dir = package_name.split('/')[0]
    if len(package_dir) == 0:
        raise Exception("Please enter a valid package name")
    try:
        os.makedirs(package_dir)
    except FileExistsError:
       raise Exception("Directory already exists")
    return package_dir

def create_file(prefix, name, text=""):
    f = open(prefix+"/"+name, "w+")
    # The prefix is the directory name when relevant,
    # if not relevant this is a no-op.
    f.write(text.format(prefix))
    f.close()

def create_package(dir_name):
    create_file(dir_name, "README.md", README_TEXT)
    create_file(dir_name, "LICENSE.txt", MIT_LISCENSE)
    create_file(dir_name, "setup.py", SETUP_TEXT)
    subdir = dir_name+"/"+dir_name
    os.makedirs(subdir, exist_ok=True)
    create_file(subdir, "__init__.py", INIT_TEXT)
    create_file(subdir, "main.py")

def main():
    dir_name = create_dir()
    create_package(dir_name)

if __name__ == "__main__":
    main()