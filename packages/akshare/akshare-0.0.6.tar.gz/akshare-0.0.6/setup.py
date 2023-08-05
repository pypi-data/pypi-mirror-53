import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="akshare",
    version="0.0.6",
    author="Albert King",
    author_email="jindaxiang@163.com",
    description="introduction to futures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jindaxiang/fushare",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7.3',
)
