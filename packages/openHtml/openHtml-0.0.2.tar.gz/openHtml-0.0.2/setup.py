import setuptools

with open("readme.md","r",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="openHtml",
    version="0.0.2",
    author="ygunoil",
    author_email="ygunoil@163.com",
    description="auto open html",
    long_description=long_description ,
    long_description_content_type="text/markdown",
    url="https://github.com/pypi/openHtml",
    packages=setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)