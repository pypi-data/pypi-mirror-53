import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="blocksat_api",
    version="1.0.0",
    author="Will Clark",
    author_email="will8clark@gmail.com",
    description="Python bindings for Blocksat API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/willcl-ark/blockstream_blocksat",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="blockstream blocksat api",
    install_requires=requirements,
    python_requires='>=3.6',
)
