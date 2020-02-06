import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xtellixClient 0.0.2", 
    version="0.0.1",
    author="Dr Mark Amo-Boateng",
    author_email="m.amoboateng@gmail.com",
    description="A Python Client for Connecting to xtellix Optimization Servers using REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/markamo/xtellixClient",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)