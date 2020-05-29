import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="winning-links",
    version="0.0.4",
    author="olegkishenkov",
    author_email="oleg.kishenkov@gmail.com",
    description="a lightweight library for finding winning affiliate links",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/olegkishenkov/winning-links",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)