import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bihex-domedi",
    version="0.0.5",
    author="David Eduard",
    author_email="edyalex.david@gmail.com",
    description="Convert to and from multiple bases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EduardAlex/BiHex",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)