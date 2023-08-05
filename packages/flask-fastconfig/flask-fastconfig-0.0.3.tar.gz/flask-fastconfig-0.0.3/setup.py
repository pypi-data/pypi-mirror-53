import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flask-fastconfig",
    version="0.0.3",
    author="Zhou Zhiping",
    author_email="himoker@163.com",
    description="ini config model for flask",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zpzhoudev/flask-fastconfig",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
