import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mathter",
    version="0.0.2",
    author="ctbaz",
    author_email="curitibagarrett@gmail.com",
    description="Math helper package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gtwogood/mathter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
