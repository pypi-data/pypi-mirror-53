import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="protaccel",
    version="0.201",
    author="Gennady Gorin",
    author_email="ggorin@caltech.edu",
    description="Package to infer kinetics from scRNA-seq/feature barcoding data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pachterlab/GSP_2019",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)

