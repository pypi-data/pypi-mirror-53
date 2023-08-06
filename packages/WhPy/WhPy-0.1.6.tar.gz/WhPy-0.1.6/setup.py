import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="WhPy",
    version="0.1.6",
    author="Michael duBois",
    author_email="mdubois@mcduboiswebservices.com",
    description="A Python 3 webhook module.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MichaelCduBois/WhPy",
    packages=["WhPy"],
    install_requires=[
        "requests==2.22.0"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent"
    ]
)
