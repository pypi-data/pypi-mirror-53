import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='reconframe',  
    version='0.1.0',
    author="0xcrypto",
    author_email="me@ivxenog.in",
    description="A Reconnaissance Framework for Penetration Testing",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/0xcrypto/reconframe",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "reconframe = reconframe.Commands:cli",
    ]},
    python_requires='>=3.6',
)
