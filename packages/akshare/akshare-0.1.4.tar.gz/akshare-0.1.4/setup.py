import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="akshare",
    version="0.1.4",
    author="Albert King",
    author_email="jindaxiang@163.com",
    description="a tools of downloading futures data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jindaxiang/akshare",
    packages=setuptools.find_packages(),
    package_data={'': ['*.py', '*.json']},
    keywords=['futures', 'finance', 'spider'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7.3',
)
