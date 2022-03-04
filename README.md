Tools you will need to build and run this project:

 - Python 3.10
 - [poetry](https://python-poetry.org/)

To start developing/exploring this project you will need to first run 

    poetry install

Then you can build the package with

    make dist

That will run the test suite and prep a sdist and while package.

When you need to rebuild the package you can do 

    make clean
    make dist

to run tests and build the packages. See the Makefile for details.

Once those are built you can build a container image using the included Dockerfile